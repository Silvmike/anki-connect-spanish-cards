from pydantic_settings import BaseSettings
import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

class Settings(BaseSettings):
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()