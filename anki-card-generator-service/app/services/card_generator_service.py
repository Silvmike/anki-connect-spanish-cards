from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..schemas import CardRequest

class CardGenerator(ABC):
    @abstractmethod
    def create_note(self, data: CardRequest) -> Dict[str, Any]:
        pass

class AllInOneCardGenerator(CardGenerator):
    def create_note(self, data: CardRequest) -> Dict[str, Any]:
        options = [data.source_lang_sentence] + data.generated_options
        q_fields = {f"Q_{i+1}": option for i, option in enumerate(options)}
        
        answers = ["1"] + ["0"] * len(data.generated_options)
        
        return {
            "deckName": "Test",
            "modelName": "AllInOne (kprim, mc, sc)",
            "fields": {
                "Question": data.target_lang_sentence,
                "QType": "2",
                **q_fields,
                "Answers": " ".join(answers)
            }
        }

class BasicAudioCardGenerator(CardGenerator):
    def create_note(self, data: CardRequest) -> Dict[str, Any]:
        return {
            "deckName": "Test",
            "modelName": "Basic",
            "fields": {
                "Front": f"[sound:{data.audio_url}]",
                "Back": f"{data.source_lang_sentence}<br>{data.target_lang_sentence}"
            }
        }

class BasicReversedCardGenerator(CardGenerator):
    def create_note(self, data: CardRequest) -> Dict[str, Any]:
        return {
            "deckName": "Test",
            "modelName": "Basic (and reversed card)",
            "fields": {
                "Front": f"<img src=\"{data.image_url}\"/><br/>{data.source_lang_sentence}",
                "Back": data.target_lang_sentence
            }
        }

class CardFactory:
    def __init__(self):
        self._generators = {
            "all_in_one": AllInOneCardGenerator(),
            "basic_audio": BasicAudioCardGenerator(),
            "basic_reversed": BasicReversedCardGenerator(),
        }

    def create_all_notes(self, data: CardRequest) -> List[Dict[str, Any]]:
        return [gen.create_note(data) for gen in self._generators.values()]

card_factory = CardFactory()
