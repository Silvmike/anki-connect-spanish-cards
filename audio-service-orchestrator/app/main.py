import os
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from .models import GenerateAudioRequest, GenerateAudioResponseItem
from .services.audio_generation_service import AudioGenerationService
from .clients.audio_client import AudioClient
from .clients.audio_upload_client import AudioUploadClient
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

app = FastAPI()

APP_PORT = int(os.getenv("APP_PORT", "8000"))

# Initialize clients with environment variables
audio_service_host = os.getenv('AUDIO_SERVICE_HOST', 'audio-service')
audio_service_port = os.getenv('AUDIO_SERVICE_PORT', '8000')
audio_upload_host = os.getenv('AUDIO_UPLOAD_SERVICE_HOST', 'yandex-disk-service')
audio_upload_port = os.getenv('AUDIO_UPLOAD_SERVICE_PORT', '8000')

audio_client = AudioClient(
    base_url=f"http://{audio_service_host}:{audio_service_port}/"
)

google_drive_client = AudioUploadClient(
    base_url=f"http://{audio_upload_host}:{audio_upload_port}/"
)

# Initialize service
audio_generation_service = AudioGenerationService(audio_client, google_drive_client)

@app.get("/health", response_model=str)
async def get_health():
    return "OK"

@app.post("/generate-audio", response_model=List[GenerateAudioResponseItem])
async def generate_audio(request: GenerateAudioRequest):
    try:
        results = await audio_generation_service.generate_audio_files(request.query)
        if not results:
            raise HTTPException(status_code=500, detail="Failed to generate any audio files")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)