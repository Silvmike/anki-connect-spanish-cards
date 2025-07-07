from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from database import Base


class File(Base):
    __tablename__ = "files"

    file_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    inserted_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    text_value = Column(String(255), nullable=False)


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    phrase_id = Column(Integer, ForeignKey("phrases.id"), nullable=False)
    clob_value = Column(Text, nullable=False)