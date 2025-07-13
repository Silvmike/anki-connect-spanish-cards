from pydantic import BaseModel, Field
from typing import List

class CardRequest(BaseModel):
    source_lang_sentence: str = Field(..., alias="sourceLangSentence")
    target_lang_sentence: str = Field(..., alias="targetLangSentence")
    image_url: str = Field(..., alias="imageUrl")
    audio_url: str = Field(..., alias="audioUrl")
    generated_options: List[str] = Field(..., alias="generatedOptions")
