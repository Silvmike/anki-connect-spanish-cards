from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/file_phrase_card_db"

    class Config:
        env_file = ".env"


settings = Settings()