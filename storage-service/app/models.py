from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class File(Base):
    __tablename__ = "files"

    file_id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    inserted_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    text_value = Column(String, unique=True, index=True, nullable=False)

    cards = relationship("Card", back_populates="phrase")

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    phrase_id = Column(Integer, ForeignKey("phrases.id"), nullable=False)
    clob_value = Column(Text, nullable=False)

    phrase = relationship("Phrase", back_populates="cards")