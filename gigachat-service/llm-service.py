from fastapi import FastAPI, HTTPException, Response, Query
from typing import List
from pydantic import BaseModel
import uvicorn
import os
import re
import time

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

with open('.api_key', 'r') as file:
    API_KEY = file.read()

APP_PORT = int(os.getenv("APP_PORT", default="8000"))

app = FastAPI()

model = ""
giga = GigaChat(credentials=API_KEY, verify_ssl_certs=False, model=model)

@app.get("/health")
def get_health():
    return "OK"

def clean_string(s):
    return re.sub(r'^(?:-?|([^.]+\.))\s*', '', s).rstrip()

def generate_same_length_word(phrase):

    tokens = giga.tokens_count(input_=[phrase], model=model)[0].tokens

    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content=f"You're a smart assistant creating the best educational materials for language learners. "
                        f"Make up 2 to 3 phrases in Spanish that can be used to test student's knowledge having different meaning to the input phrase and having similar length to the input phrase and "
                        f"tell the user only the made up phrases. Do not generate unnecessary tokens, they cost user money."
            ),
            Messages(
                role=MessagesRole.USER,
                content=f"Random seed: {round(time.time() * 1000)}\n"
                        f"Input phrase: \n{phrase}\n\n"
                        f"Output phrases: "
            )
        ],
        temperature=0.9,
        max_tokens=3 * (tokens + 15),
    )

    response = giga.chat(payload)
    results = response.choices[0].message.content.strip().split("\n\n")[0].split("\n")
    return [clean_string(x) for x in results]

def count_words(text):
    words = text.split()
    return len(words)

def generate_cloze_deletion(phrase, translation):

    tokens = giga.tokens_count(input_=[phrase], model=model)[0].tokens
    word_count = count_words(phrase)

    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content="You're a smart assistant creating the best educational materials for language learners. "
                        "Make up a [cloze deletion] card for Anki from input [phrase]. "
                        "Example for 'a la derecha': a {{c1:la}} {{c2:derecha}}. "
                        "Do not generate unnecessary tokens, they cost user money."
            ),
            Messages(
                role=MessagesRole.USER,
                content=f"Random seed: {round(time.time() * 1000)}\n"
                        f"Input [phrase]: {phrase}\n"
                        f"Output [cloze deletion]: "
            )
        ],
        temperature=0.9,
        max_tokens=tokens + (word_count * 10),
    )

    response = giga.chat(payload)
    return f"{translation}: {response.choices[0].message.content}"

class ParaphraseRequest(BaseModel):
    input: str

class ParaphraseResponse(BaseModel):
    output: List[str]

@app.post("/generate-answers")
def post_sample(request: ParaphraseRequest):
    result = generate_same_length_word(request.input)
    return ParaphraseResponse(output=result)


class ClozeDeletionRequest(BaseModel):
    input: str
    translation: str

@app.post("/cloze-deletion")
def cloze_deletion(request: ClozeDeletionRequest):
    return generate_cloze_deletion(request.input, request.translation)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)