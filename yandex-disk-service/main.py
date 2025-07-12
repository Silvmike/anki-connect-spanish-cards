# Token for 365 days can be obtained manually https://yandex.ru/dev/disk-api/doc/ru/concepts/quickstart#quickstart__oauth
# Token should be placed in token.json { "token": ... }

import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import yadisk
import uvicorn
import json
import traceback

APP_PORT = int(os.getenv("APP_PORT", default="8000"))

app = FastAPI(
    title="File Service",
    description="A REST API to publish and delete files."
)

# --- Configuration ---
YANDEX_DISK_TOKEN = None
YANDEX_FILE_DIR = 'anki-audio'
TOKEN_FILE_PATH = 'token.json'

try:
    with open(TOKEN_FILE_PATH, 'r') as f:
        token_data = json.load(f)
        YANDEX_DISK_TOKEN = token_data.get('token')
    if not YANDEX_DISK_TOKEN:
        raise ValueError(f"'{TOKEN_FILE_PATH}' found, but 'token' key is missing or empty.")
except FileNotFoundError:
    raise RuntimeError(f"Error: '{TOKEN_FILE_PATH}' not found. Please create this file with your Yandex Disk OAuth token.")
except json.JSONDecodeError:
    raise RuntimeError(f"Error: Could not decode JSON from '{TOKEN_FILE_PATH}'. Please ensure it's valid JSON.")
except Exception as e:
    raise RuntimeError(f"An unexpected error occurred while reading '{TOKEN_FILE_PATH}': {e}")

if not YANDEX_DISK_TOKEN: # This check is redundant after the try-except block, but kept for clarity
    raise ValueError("Yandex Disk OAuth token is not configured. Please set YANDEX_DISK_TOKEN.")

# Initialize YaDisk client
# Ensure the token is set before initializing, or handle the error gracefully.
if not YANDEX_DISK_TOKEN or YANDEX_DISK_TOKEN == 'YOUR_YANDEX_DISK_OAUTH_TOKEN':
    raise ValueError("Yandex Disk OAuth token is not configured. Please set YANDEX_DISK_TOKEN.")

disk = yadisk.AsyncClient("de885c5f174d4c54a11094f8e3e0757a", "0b6ff3b7d9b14ed09b76d8f77bfd6e67", YANDEX_DISK_TOKEN)

if disk.check_token() is False:
    raise RuntimeError("Provided token is invalid!")

# --- FastAPI Endpoints ---

@app.get("/health")
async def get_health():
    return "OK"

@app.post("/upload", summary="Upload and publish a file")
async def upload_file(
    file: UploadFile = File(..., description="The file to upload.")
):
    """
    Uploads a file to Yandex Disk, makes it public, and returns its public URL.

    - **file**: The file to be uploaded.
    """
    yandex_path = f"/{YANDEX_FILE_DIR}/{file.filename}"

    try:
        if await disk.exists(yandex_path):
            raise HTTPException(
                status_code=409,
                detail=f"File '{yandex_path}' already exists."
            )

        # Upload the file
        # yadisk.upload() takes a file-like object or a path to a local file.
        # UploadFile.file is a SpooledTemporaryFile, which is a file-like object.
        await disk.upload(file.file, yandex_path, overwrite=True)

        # Make the file public
        await disk.publish(yandex_path)

        # Obtain public url
        public_url = await disk.get_download_link(yandex_path)

        if public_url:
            return JSONResponse(content={
                "message": "File uploaded and published successfully",
                "filename": file.filename,
                "url": public_url
            }, status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Failed to publish file on Yandex Disk.")

    except Exception as e:
        stack_trace_string = traceback.format_exc()
        print(f"An unexpected error occurred during file upload and publish: {e} {stack_trace_string}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@app.delete("/delete", summary="Delete a file")
async def delete_file(filename: str, permanently: bool = True):
    """
    Deletes a file from Yandex Disk.

    - **filename**: The file name.
    - **permanently**: If True, the file is deleted permanently without moving to trash.
      Defaults to True.
    """
    yandex_path = f"/{YANDEX_FILE_DIR}/{filename}"

    try:
        # Check if the file exists before attempting to delete
        if not await disk.exists(yandex_path):
            raise HTTPException(status_code=404, detail=f"File '{yandex_path}' not found on Yandex Disk.")

        await disk.remove(yandex_path, permanently=permanently)
        print(f"File '{yandex_path}' deleted successfully.")
        return JSONResponse(content={
            "message": f"File '{yandex_path}' deleted successfully"
        }, status_code=200)

    except Exception as e:
        print(f"An unexpected error occurred during file deletion: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

# --- Running the FastAPI App ---
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)