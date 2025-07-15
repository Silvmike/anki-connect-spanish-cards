from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import os
import io
from gtts import gTTS

APP_PORT = int(os.getenv("APP_PORT", default="8000"))
app = FastAPI()


@app.get("/health")
def get_health():
    return "OK"


class GenerateAudioRequest(BaseModel):
    query: str
    lang: str = "es"


@app.post("/generate")
async def generate(request: GenerateAudioRequest):
    try:
        audio_data = io.BytesIO()
        tts = gTTS(text=request.query, lang=request.lang)
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        return StreamingResponse(audio_data, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
