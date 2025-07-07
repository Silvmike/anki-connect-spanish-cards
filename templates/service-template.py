from fastapi import FastAPI, HTTPException, Response, Query
from pydantic import BaseModel
import uvicorn
import os
import asyncio

APP_PORT = int(os.getenv("APP_PORT", default="8000"))

app = FastAPI()

@app.get("/health")
def get_health():
    return "OK"

# your code here

class SimpleRequest(BaseModel):
    input: str

class SimpleResponse(BaseModel):
    output: str

@app.post("/sample")
async def post_sample(request: SimpleRequest):
    await asyncio.sleep(2)
    return SimpleResponse(output=request.input)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)