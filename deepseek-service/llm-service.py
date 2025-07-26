from fastapi import FastAPI, HTTPException, Response, Query
from typing import List
from pydantic import BaseModel
import uvicorn
import os
import re
import time
import openai

try:
    with open('.api_key', 'r') as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    raise ValueError("DeepSeek API key not found. Please create a .api_key file or set DEEPSEEK_API_KEY environment variable.")


APP_PORT = int(os.getenv("APP_PORT", default="8000"))

app = FastAPI()

client = openai.OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
model = "deepseek-chat"

@app.get("/health")
def get_health():
    return "OK"

def clean_string(s):
    return re.sub(r'^(?:-?|([^.]+\.))\s*', '', s).rstrip()

def generate_same_length_word(phrase):
    messages = [
        {
            "role": "system",
            "content": f"You're a smart assistant creating the best educational materials for language learners. "
                       f"Make up 2 to 3 phrases in Spanish that can be used to test student's knowledge having different meaning to the input phrase and having similar length to the input phrase and "
                       f"tell the user only the made up phrases. Do not generate unnecessary tokens, they cost user money."
        },
        {
            "role": "user",
            "content": f"Random seed: {round(time.time() * 1000)}\n"
                       f"Input phrase: \n{phrase}\n\n"
                       f"Output phrases: "
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.9,
        max_tokens=100
    )
    
    results = response.choices[0].message.content.strip().split("\n\n")[0].split("\n")
    return [clean_string(x) for x in results if x]

def count_words(text):
    words = text.split()
    return len(words)

def generate_cloze_deletion(phrase, translation):
    messages = [
        {
            "role": "system",
            "content": "You're a smart assistant creating the best educational materials for language learners. "
                       "Make up a [cloze deletion] card for Anki from input [phrase]. "
                       "Example for 'a la derecha': a {{c1::la}} {{c2::derecha}}. "
                       "Do not generate unnecessary tokens, they cost user money."
        },
        {
            "role": "user",
            "content": f"Random seed: {round(time.time() * 1000)}\n"
                       f"Input [phrase]: {phrase}\n"
                       f"Output [cloze deletion]: "
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.9,
        max_tokens=len(phrase.split()) * 20
    )
    
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
