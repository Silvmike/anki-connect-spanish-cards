import os
import io
import hashlib
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Response, Query
from fastapi.responses import JSONResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import uvicorn

app = FastAPI()

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
CACHE_DIR = 'file_cache'
CACHE_EXPIRE_SECONDS = 3600  # 1 hour cache duration

# Ensure cache directory exists
Path(CACHE_DIR).mkdir(exist_ok=True)


def get_drive_service():
    """Initialize and return Google Drive service"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def get_cache_path(file_id: str) -> Path:
    """Generate consistent cache file path based on file ID"""
    # Hash the file_id to create a safe filename
    filename = hashlib.md5(file_id.encode()).hexdigest()
    return Path(CACHE_DIR) / filename


def is_cache_valid(cache_path: Path) -> bool:
    """Check if cached file exists and hasn't expired"""
    if not cache_path.exists():
        return False

    file_age = os.path.getmtime(cache_path)
    current_time = os.path.getmtime(__file__)  # Using this file's mtime as reference
    return (current_time - file_age) < CACHE_EXPIRE_SECONDS


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to Google Drive after checking existence"""
    try:
        service = get_drive_service()

        # Check if file exists
        query = f"name='{file.filename}' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if items:
            return JSONResponse(
                status_code=200,
                content={
                    'message': 'File already exists',
                    'file_id': items[0]['id'],
                    'file_name': items[0]['name']
                }
            )

        # Upload the file
        contents = await file.read()
        file_metadata = {'name': file.filename, 'mimeType': file.content_type}
        media = MediaIoBaseUpload(io.BytesIO(contents),
                                  mimetype=file.content_type,
                                  resumable=True)

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name'
        ).execute()

        return JSONResponse(
            status_code=201,
            content={
                'message': 'File uploaded successfully',
                'file_id': uploaded_file.get('id'),
                'file_name': uploaded_file.get('name')
            }
        )

    except HttpError as error:
        raise HTTPException(status_code=500, detail=f'Drive API error: {error}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')


@app.get("/download/{file_id}")
async def download_file(
        file_id: str,
        force_refresh: bool = Query(False, description="Bypass cache and fetch fresh from Drive")
):
    """Download a file from Google Drive or local cache"""
    cache_path = get_cache_path(file_id)

    # Serve from cache if available and not forcing refresh
    if not force_refresh and is_cache_valid(cache_path):
        try:
            with open(cache_path, 'rb') as cached_file:
                content = cached_file.read()

            # Get metadata from cache
            metadata_path = cache_path.with_suffix('.meta')
            if metadata_path.exists():
                with open(metadata_path, 'r') as meta_file:
                    metadata = meta_file.read().splitlines()
                    if len(metadata) >= 2:
                        return Response(
                            content=content,
                            media_type=metadata[0],
                            headers={"Content-Disposition": f"attachment; filename={metadata[1]}"}
                        )

            # Fallback to generic response if metadata is missing
            return Response(content=content, media_type="application/octet-stream")

        except Exception as e:
            # If cache read fails, proceed to download from Drive
            pass

    # Download from Google Drive
    try:
        service = get_drive_service()

        # Get file metadata
        file_metadata = service.files().get(
            fileId=file_id,
            fields='name,mimeType'
        ).execute()

        # Download file content
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        content = fh.getvalue()

        # Save to cache
        with open(cache_path, 'wb') as cache_file:
            cache_file.write(content)

        # Save metadata
        metadata_path = cache_path.with_suffix('.meta')
        with open(metadata_path, 'w') as meta_file:
            meta_file.write(f"{file_metadata['mimeType']}\n{file_metadata['name']}")

        return Response(
            content=content,
            media_type=file_metadata['mimeType'],
            headers={"Content-Disposition": f"attachment; filename={file_metadata['name']}"}
        )

    except HttpError as error:
        if error.resp.status == 404:
            raise HTTPException(status_code=404, detail="File not found in Google Drive")
        raise HTTPException(status_code=500, detail=f'Drive API error: {error}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)