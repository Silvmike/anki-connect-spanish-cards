from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# File Schemas
class FileBase(BaseModel):
    name: str

class FileCreate(FileBase):
    pass

class FileUpdate(FileBase):
    pass

class File(FileBase):
    file_id: int
    inserted_at: datetime

    class Config:
        from_attributes = True

# Phrase Schemas
class PhraseBase(BaseModel):
    text_value: str

class PhraseCreate(PhraseBase):
    pass

class PhraseUpdate(PhraseBase):
    pass

class Phrase(PhraseBase):
    id: int

    class Config:
        from_attributes = True

# Card Schemas
class CardBase(BaseModel):
    phrase_id: int
    clob_value: str

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class Card(CardBase):
    id: int

    class Config:
        from_attributes = True