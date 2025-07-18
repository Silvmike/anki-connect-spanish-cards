from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import uuid
import os

from .anki_connect_service import AnkiConnectService
from ..schemas import CardRequest

STORAGE_MODE_ANKI = "ANKI"
STORAGE_MODE_URL = "URL"

STORAGE_MODE = os.getenv("STORAGE_MODE", STORAGE_MODE_ANKI)

class CardGenerator(ABC):
    @abstractmethod
    def create_note(self, data: CardRequest, anki_service: Optional[AnkiConnectService] = None) -> Dict[str, Any]:
        pass

    def available(self) -> bool:
        return True

class AllInOneCardGenerator(CardGenerator):
    def create_note(self, data: CardRequest, anki_service: Optional[AnkiConnectService] = None) -> Dict[str, Any]:
        options = [data.source_lang_sentence] + data.generated_options
        q_fields = {f"Q_{i+1}": option for i, option in enumerate(options)}

        answers = ["1"] + ["0"] * len(data.generated_options)

        return {
            "deckName": data.deck_name,
            "modelName": "AllInOne (kprim, mc, sc)",
            "fields": {
                "Question": data.target_lang_sentence,
                "QType": "2",
                **q_fields,
                "Answers": " ".join(answers)
            }
        }


class BasicAudioCardGeneratorAnki(CardGenerator):
    def create_note(self, data: CardRequest, anki_service: Optional[AnkiConnectService] = None) -> Dict[str, Any]:
        if not anki_service:
            raise ValueError("AnkiConnectService is required for BasicAudioCardGenerator")

        original_filename = data.audio_url.split('/')[-1]
        _, extension = os.path.splitext(original_filename)
        filename = f"{uuid.uuid4()}{extension}"
        stored_filename = anki_service.store_media_file_from_url(filename, data.audio_url)
        return {
            "deckName": data.deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": f"[sound:{stored_filename}]",
                "Back": f"{data.source_lang_sentence}<br>{data.target_lang_sentence}"
            }
        }

    def available(self) -> bool:
        return STORAGE_MODE == STORAGE_MODE_ANKI

class BasicAudioCardGeneratorUrl(CardGenerator):
    def create_note(self, data: CardRequest, anki_service: Optional[AnkiConnectService] = None) -> Dict[str, Any]:
        return {
            "deckName": data.deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": f"[sound:{data.audio_url}]",
                "Back": f"{data.source_lang_sentence}<br>{data.target_lang_sentence}"
            }
        }

    def available(self) -> bool:
        return STORAGE_MODE == STORAGE_MODE_URL

class BasicReversedCardGeneratorUrl(CardGenerator):
    def create_note(self, data: CardRequest, anki_service: Optional[AnkiConnectService] = None) -> Dict[str, Any]:
        return {
            "deckName": data.deck_name,
            "modelName": "Basic (and reversed card)",
            "fields": {
                "Front": f"<img src=\"{data.image_url}\"/><br/>{data.source_lang_sentence}",
                "Back": data.target_lang_sentence
            }
        }

    def available(self) -> bool:
        return STORAGE_MODE == STORAGE_MODE_URL

class BasicReversedCardGeneratorAnki(CardGenerator):
    def create_note(self, data: CardRequest, anki_service: Optional[AnkiConnectService] = None) -> Dict[str, Any]:
        if not anki_service:
            raise ValueError("AnkiConnectService is required for BasicReversedCardGenerator")

        original_filename = data.image_url.split('/')[-1]
        _, extension = os.path.splitext(original_filename)
        filename = f"{uuid.uuid4()}{extension}"
        stored_filename = anki_service.store_media_file_from_url(filename, data.image_url)
        return {
            "deckName": data.deck_name,
            "modelName": "Basic (and reversed card)",
            "fields": {
                "Front": f"<img src=\"{stored_filename}\"/><br/>{data.source_lang_sentence}",
                "Back": data.target_lang_sentence
            }
        }

    def available(self) -> bool:
        return STORAGE_MODE == STORAGE_MODE_ANKI


class CardFactory:
    def __init__(self):
        self._generators = {
            "all_in_one": AllInOneCardGenerator(),
            "basic_audio_anki": BasicAudioCardGeneratorAnki(),
            "basic_audio_url": BasicAudioCardGeneratorUrl(),
            "basic_reversed_anki": BasicReversedCardGeneratorAnki(),
            "basic_reversed_url": BasicReversedCardGeneratorUrl(),
        }

    def create_all_notes(self, data: CardRequest, anki_service: AnkiConnectService) -> List[Dict[str, Any]]:
        available_generators = [gen for gen in self._generators.values() if gen.available()]
        return [gen.create_note(data, anki_service=anki_service) for gen in available_generators]


card_factory = CardFactory()
