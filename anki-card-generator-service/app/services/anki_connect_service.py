import requests
from ..config import ANKI_CONNECT_URL
from typing import Dict, Any, List

class AnkiConnectService:
    def __init__(self, url: str = ANKI_CONNECT_URL):
        self.url = url

    def _invoke(self, action: str, **params) -> Dict[str, Any]:
        payload = {"action": action, "version": 6, "params": params}
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                raise Exception(f"AnkiConnect error: {result['error']}")
            return result["result"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to AnkiConnect: {e}")

    def add_note(self, note: Dict[str, Any]) -> int:
        return self._invoke("addNote", note=note)

    def sync(self) -> None:
        self._invoke("sync")

    def get_deck_names(self) -> List[str]:
        return self._invoke("deckNames")

    def get_model_names(self) -> List[str]:
        return self._invoke("modelNames")

    def create_deck(self, deck: str) -> int:
        return self._invoke("createDeck", deck=deck)

    def store_media_file_from_url(self, filename: str, url: str) -> str:
        return self._invoke("storeMediaFile", filename=filename, url=url)
