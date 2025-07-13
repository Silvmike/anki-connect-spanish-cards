import os
from dotenv import load_dotenv

load_dotenv()

APP_PORT = int(os.getenv("APP_PORT", 8000))
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL", "http://host.docker.internal:8765")
