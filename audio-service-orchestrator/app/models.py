from pydantic import BaseModel

class GenerateAudioRequest(BaseModel):
    query: str

class GenerateAudioResponseItem(BaseModel):
    url: str
    speaker: str