from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
import uvicorn
import os
import asyncio

APP_PORT = int(os.getenv("APP_PORT", default="8000"))

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# File endpoints
@app.post("/files/", response_model=schemas.File)
def create_file(file: schemas.FileCreate, db: Session = Depends(get_db)):
    return crud.create_file(db=db, file=file)

@app.get("/files/{file_id}", response_model=schemas.File)
def read_file(file_id: int, db: Session = Depends(get_db)):
    db_file = crud.get_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@app.put("/files/{file_id}", response_model=schemas.File)
def update_file(file_id: int, file: schemas.FileCreate, db: Session = Depends(get_db)):
    db_file = crud.update_file(db, file_id=file_id, file=file)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@app.delete("/files/{file_id}", response_model=schemas.File)
def delete_file(file_id: int, db: Session = Depends(get_db)):
    db_file = crud.delete_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

# Phrase endpoints
@app.post("/phrases/", response_model=schemas.Phrase)
def create_phrase(phrase: schemas.PhraseCreate, db: Session = Depends(get_db)):
    return crud.create_phrase(db=db, phrase=phrase)

@app.get("/phrases/{phrase_id}", response_model=schemas.Phrase)
def read_phrase(phrase_id: int, db: Session = Depends(get_db)):
    db_phrase = crud.get_phrase(db, phrase_id=phrase_id)
    if db_phrase is None:
        raise HTTPException(status_code=404, detail="Phrase not found")
    return db_phrase

@app.put("/phrases/{phrase_id}", response_model=schemas.Phrase)
def update_phrase(phrase_id: int, phrase: schemas.PhraseCreate, db: Session = Depends(get_db)):
    db_phrase = crud.update_phrase(db, phrase_id=phrase_id, phrase=phrase)
    if db_phrase is None:
        raise HTTPException(status_code=404, detail="Phrase not found")
    return db_phrase

@app.delete("/phrases/{phrase_id}", response_model=schemas.Phrase)
def delete_phrase(phrase_id: int, db: Session = Depends(get_db)):
    db_phrase = crud.delete_phrase(db, phrase_id=phrase_id)
    if db_phrase is None:
        raise HTTPException(status_code=404, detail="Phrase not found")
    return db_phrase

# Card endpoints
@app.post("/cards/", response_model=schemas.Card)
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    return crud.create_card(db=db, card=card)

@app.get("/cards/{card_id}", response_model=schemas.Card)
def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.get_card(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@app.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, card: schemas.CardCreate, db: Session = Depends(get_db)):
    db_card = crud.update_card(db, card_id=card_id, card=card)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@app.delete("/cards/{card_id}", response_model=schemas.Card)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.delete_card(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

# Search endpoints
@app.get("/search/phrase/exact_by_text_value", response_model=List[schemas.Phrase])
def search_phrase_exact(text_value: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_phrases_exact(db, text_value=text_value)

@app.get("/search/phrase/like_by_text_value", response_model=List[schemas.Phrase])
def search_phrase_like(text_pattern: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_phrases_like(db, text_pattern=text_pattern)

@app.get("/search/file/exact_by_name", response_model=List[schemas.File])
def search_file_exact(name: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_files_exact(db, name=name)

@app.get("/search/file/like_by_name", response_model=List[schemas.File])
def search_file_like(name_pattern: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_files_like(db, name_pattern=name_pattern)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)