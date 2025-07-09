# app/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    DATABASE_URL: str = "postgresql://user:password@db:5432/mydatabase" # Default for local testing without explicit env var
    APP_PORT: int = 8000 # Default for local testing without explicit env var

    # We remove 'env_file=".env"' from here
    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()