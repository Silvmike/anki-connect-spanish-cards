import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import init_db, get_db
from app import models, schemas
from app.config import settings

app = FastAPI()

@app.on_event("startup")
def on_startup():
    """
    Initializes the database tables on application startup.
    """
    init_db()

@app.get("/health")
def get_health():
    return "OK"

# --- File Resources ---

@app.post("/files/", response_model=schemas.File, status_code=status.HTTP_201_CREATED)
def create_file(file: schemas.FileCreate, db: Session = Depends(get_db)):
    db_file = models.File(name=file.name)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


@app.get("/files/{file_id}", response_model=schemas.File)
def get_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.file_id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return db_file


@app.get("/files/", response_model=List[schemas.File])
def get_all_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = db.query(models.File).offset(skip).limit(limit).all()
    return files


@app.put("/files/{file_id}", response_model=schemas.File)
def update_file(file_id: int, file: schemas.FileUpdate, db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.file_id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    db_file.name = file.name
    db.commit()
    db.refresh(db_file)
    return db_file


@app.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.file_id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    db.delete(db_file)
    db.commit()
    return {"detail": "File deleted"}


# --- Phrase Resources ---

@app.post("/phrases/", response_model=schemas.Phrase, status_code=status.HTTP_201_CREATED)
def create_phrase(phrase: schemas.PhraseCreate, db: Session = Depends(get_db)):
    db_phrase = models.Phrase(text_value=phrase.text_value)
    db.add(db_phrase)
    db.commit()
    db.refresh(db_phrase)
    return db_phrase


@app.get("/phrases/{phrase_id}", response_model=schemas.Phrase)
def get_phrase(phrase_id: int, db: Session = Depends(get_db)):
    db_phrase = db.query(models.Phrase).filter(models.Phrase.id == phrase_id).first()
    if db_phrase is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phrase not found")
    return db_phrase


@app.get("/phrases/", response_model=List[schemas.Phrase])
def get_all_phrases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    phrases = db.query(models.Phrase).offset(skip).limit(limit).all()
    return phrases


@app.put("/phrases/{phrase_id}", response_model=schemas.Phrase)
def update_phrase(phrase_id: int, phrase: schemas.PhraseUpdate, db: Session = Depends(get_db)):
    db_phrase = db.query(models.Phrase).filter(models.Phrase.id == phrase_id).first()
    if db_phrase is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phrase not found")

    db_phrase.text_value = phrase.text_value
    db.commit()
    db.refresh(db_phrase)
    return db_phrase


@app.delete("/phrases/{phrase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_phrase(phrase_id: int, db: Session = Depends(get_db)):
    db_phrase = db.query(models.Phrase).filter(models.Phrase.id == phrase_id).first()
    if db_phrase is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phrase not found")

    db.delete(db_phrase)
    db.commit()
    return {"detail": "Phrase deleted"}


# --- Card Resources ---

@app.post("/cards/", response_model=schemas.Card, status_code=status.HTTP_201_CREATED)
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    # Check if phrase_id exists
    db_phrase = db.query(models.Phrase).filter(models.Phrase.id == card.phrase_id).first()
    if db_phrase is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phrase ID does not exist")

    db_card = models.Card(phrase_id=card.phrase_id, clob_value=card.clob_value)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@app.get("/cards/{card_id}", response_model=schemas.Card)
def get_card(card_id: int, db: Session = Depends(get_db)):
    db_card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return db_card


@app.get("/cards/", response_model=List[schemas.Card])
def get_all_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cards = db.query(models.Card).offset(skip).limit(limit).all()
    return cards


@app.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, card: schemas.CardUpdate, db: Session = Depends(get_db)):
    db_card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")

    # Check if phrase_id exists if it's being updated
    if card.phrase_id != db_card.phrase_id:
        db_phrase = db.query(models.Phrase).filter(models.Phrase.id == card.phrase_id).first()
        if db_phrase is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phrase ID does not exist")

    db_card.phrase_id = card.phrase_id
    db_card.clob_value = card.clob_value
    db.commit()
    db.refresh(db_card)
    return db_card


@app.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")

    db.delete(db_card)
    db.commit()
    return {"detail": "Card deleted"}


# --- Specific Search Services ---

@app.get("/search/phrase/exact_by_text_value", response_model=List[schemas.Phrase])
def search_phrase_exact_by_text_value(
        text_value: str = Query(..., description="Exact text value to search for"),
        db: Session = Depends(get_db)
):
    phrases = db.query(models.Phrase).filter(models.Phrase.text_value == text_value).all()
    return phrases


@app.get("/search/phrase/like_by_text_value", response_model=List[schemas.Phrase])
def search_phrase_like_by_text_value(
        text_value: str = Query(...,
                                description="Text value (case-insensitive, partial match) to search for with LIKE"),
        db: Session = Depends(get_db)
):
    # For case-insensitive LIKE, convert both to lower case
    phrases = db.query(models.Phrase).filter(models.Phrase.text_value.ilike(f"%{text_value}%")).all()
    return phrases


@app.get("/search/file/exact_by_name", response_model=List[schemas.File])
def search_file_exact_by_name(
        name: str = Query(..., description="Exact file name to search for"),
        db: Session = Depends(get_db)
):
    files = db.query(models.File).filter(models.File.name == name).all()
    return files


@app.get("/search/file/like_by_name", response_model=List[schemas.File])
def search_file_like_by_name(
        name: str = Query(..., description="File name (case-insensitive, partial match) to search for with LIKE"),
        db: Session = Depends(get_db)
):
    files = db.query(models.File).filter(models.File.name.ilike(f"%{name}%")).all()
    return files


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
