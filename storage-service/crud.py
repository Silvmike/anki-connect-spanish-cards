from sqlalchemy.orm import Session
from . import models, schemas

# File CRUD operations
def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.file_id == file_id).first()

def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.File).offset(skip).limit(limit).all()

def create_file(db: Session, file: schemas.FileCreate):
    db_file = models.File(name=file.name)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def update_file(db: Session, file_id: int, file: schemas.FileCreate):
    db_file = get_file(db, file_id)
    if db_file:
        db_file.name = file.name
        db.commit()
        db.refresh(db_file)
    return db_file

def delete_file(db: Session, file_id: int):
    db_file = get_file(db, file_id)
    if db_file:
        db.delete(db_file)
        db.commit()
    return db_file

def search_files_exact(db: Session, name: str):
    return db.query(models.File).filter(models.File.name == name).all()

def search_files_like(db: Session, name_pattern: str):
    return db.query(models.File).filter(models.File.name.like(f"%{name_pattern}%")).all()

# Phrase CRUD operations
def get_phrase(db: Session, phrase_id: int):
    return db.query(models.Phrase).filter(models.Phrase.id == phrase_id).first()

def get_phrases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Phrase).offset(skip).limit(limit).all()

def create_phrase(db: Session, phrase: schemas.PhraseCreate):
    db_phrase = models.Phrase(text_value=phrase.text_value)
    db.add(db_phrase)
    db.commit()
    db.refresh(db_phrase)
    return db_phrase

def update_phrase(db: Session, phrase_id: int, phrase: schemas.PhraseCreate):
    db_phrase = get_phrase(db, phrase_id)
    if db_phrase:
        db_phrase.text_value = phrase.text_value
        db.commit()
        db.refresh(db_phrase)
    return db_phrase

def delete_phrase(db: Session, phrase_id: int):
    db_phrase = get_phrase(db, phrase_id)
    if db_phrase:
        db.delete(db_phrase)
        db.commit()
    return db_phrase

def search_phrases_exact(db: Session, text_value: str):
    return db.query(models.Phrase).filter(models.Phrase.text_value == text_value).all()

def search_phrases_like(db: Session, text_pattern: str):
    return db.query(models.Phrase).filter(models.Phrase.text_value.like(f"%{text_pattern}%")).all()

# Card CRUD operations
def get_card(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()

def get_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Card).offset(skip).limit(limit).all()

def create_card(db: Session, card: schemas.CardCreate):
    db_card = models.Card(phrase_id=card.phrase_id, clob_value=card.clob_value)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def update_card(db: Session, card_id: int, card: schemas.CardCreate):
    db_card = get_card(db, card_id)
    if db_card:
        db_card.phrase_id = card.phrase_id
        db_card.clob_value = card.clob_value
        db.commit()
        db.refresh(db_card)
    return db_card

def delete_card(db: Session, card_id: int):
    db_card = get_card(db, card_id)
    if db_card:
        db.delete(db_card)
        db.commit()
    return db_card