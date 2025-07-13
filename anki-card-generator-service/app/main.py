from fastapi import FastAPI, HTTPException, Depends
from .schemas import CardRequest
from .services.anki_connect_service import AnkiConnectService
from .services.card_generator_service import card_factory
from .config import APP_PORT
import traceback
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

def get_anki_connect_service():
    return AnkiConnectService()

@app.get("/decks")
async def get_deck_names(anki_service: AnkiConnectService = Depends(get_anki_connect_service)):
    try:
        anki_service.sync()
        return anki_service.get_deck_names()
    except Exception as e:
        stack_trace_string = traceback.format_exc()
        logger.error(f"Error adding cards: {str(e)} {stack_trace_string}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-cards")
async def generate_cards(
    request: CardRequest,
    anki_service: AnkiConnectService = Depends(get_anki_connect_service)
):
    try:
        # Check if deck exists, create if not
        if request.deck_name not in anki_service.get_deck_names():
            anki_service.create_deck(request.deck_name)

        # Check for required models
        available_models = anki_service.get_model_names()
        required_models = ["AllInOne (kprim, mc, sc)", "Basic", "Basic (and reversed card)"]
        for model in required_models:
            if model not in available_models:
                raise HTTPException(
                    status_code=400,
                    detail=f"Anki model '{model}' not found. Please ensure it is installed."
                )

        notes = card_factory.create_all_notes(request)
        added_notes_ids = []
        for note in notes:
            note_id = anki_service.add_note(note)
            added_notes_ids.append(note_id)

        anki_service.sync()

        return {
            "message": "Cards generated and synced successfully!",
            "added_notes_ids": added_notes_ids
        }
    except Exception as e:
        stack_trace_string = traceback.format_exc()
        logger.error(f"Error adding cards: {str(e)} {stack_trace_string}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def get_health():
    return "OK"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
