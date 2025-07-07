from fastapi import FastAPI, HTTPException, Response, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import os
import io

import torch
from TTS.api import TTS

os.environ["COQUI_TOS_AGREED"] = "1"

APP_PORT = int(os.getenv("APP_PORT", default="8000"))
app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

print(tts.list_models())
print(tts.speakers)


@app.get("/health")
def get_health():
    return "OK"


# Speakers:
#
# Craig Gutsy
# Barbora MacLean
# Gilberto Mathias
# Annmarie Nele
# Maja Ruoho
# Ana Florence

@app.get("/generate")
async def generate(
        query: str = Query(..., description="Input text"),
        lang: str = Query("es", description="Input language"),
        speaker: str = Query("Maja Ruoho")):
    audio_data = io.BytesIO()
    tts.tts_to_file(
        text=query,
        file_path=audio_data,
        language=lang,
        speaker=speaker
    )

    return StreamingResponse(audio_data, media_type="audio/wav")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
