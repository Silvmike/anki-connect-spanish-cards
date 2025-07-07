from fastapi import FastAPI, HTTPException, Response, Query
from pydantic import BaseModel
import uvicorn
import os

from googletrans import Translator

translator = Translator()

APP_PORT = int(os.getenv("APP_PORT", default="8000"))

app = FastAPI()

@app.get("/health")
def get_health():
    return "OK"

# your code here

class TranslateRequest(BaseModel):
    src: str = 'es'
    dest: str = 'ru'
    input: str

class TranslateResponse(BaseModel):
    text: str
    pronunciation: str

@app.post("/translate")
async def translate(request: TranslateRequest):
    output = await translator.translate(request.input, src=request.src, dest=request.dest)
    return TranslateResponse(text=output.text, pronunciation=output.pronunciation)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)