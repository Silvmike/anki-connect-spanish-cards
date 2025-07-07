from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class FileBase(BaseModel):
    name: str


class FileCreate(FileBase):
    pass


class File(FileBase):
    file_id: int
    inserted_at: datetime

    class Config:
        orm_mode = True


class PhraseBase(BaseModel):
    text_value: str


class PhraseCreate(PhraseBase):
    pass


class Phrase(PhraseBase):
    id: int

    class Config:
        orm_mode = True


class CardBase(BaseModel):
    phrase_id: int
    clob_value: str


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int

    class Config:
        orm_mode = True