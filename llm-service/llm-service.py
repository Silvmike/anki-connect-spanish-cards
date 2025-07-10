from fastapi import FastAPI, HTTPException, Response, Query
from typing import List
from pydantic import BaseModel
import uvicorn
import os
import re

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from torch.profiler import profile, ProfilerActivity

APP_PORT = int(os.getenv("APP_PORT", default="8000"))

app = FastAPI()

@app.get("/health")
def get_health():
    return "OK"

model_name = "microsoft/phi-3-mini-4k-instruct"

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    trust_remote_code=True,
    device_map=device
)

def generate_same_length_word(phrase):
    prompt = (
        f"You're a smart assistant creating the best educational materials for language learners. "
        f"Make up 2 to 3 phrases in Spanish that can be used to test student's knowledge having different meaning to the input phrase and having similar length to the input phrase and "
        f"tell the user only the made up phrases. Do not generate unnecessary tokens, they cost user money.\n\n"
        f"Input phrase: \n{phrase}\n\n"
        f"Output phrases: "
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=(3 * (len(inputs.input_ids) + 15)),
        do_sample=True,
        temperature=0.7,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0])
    results = response.replace(prompt, "").strip().split("\n\n")[0].split("\n")
    return [clean_string(x) for x in results]

def clean_string(s):
    return re.sub(r'^[^.]+\.\s*', '', s)

class ParaphraseRequest(BaseModel):
    input: str

class ParaphraseResponse(BaseModel):
    output: List[str]

@app.post("/generate-answers")
def post_sample(request: ParaphraseRequest):
    result = generate_same_length_word(request.input)
    return ParaphraseResponse(output=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)