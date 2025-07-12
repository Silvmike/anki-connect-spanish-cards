import requests
from fastapi import FastAPI, Query, Response
from pydantic import BaseModel
from typing import List
import uvicorn
import os

with open('.google_api_key', 'r') as file:
    API_KEY = file.read()

with open('.search_engine_id', 'r') as file:
    SEARCH_ENGINE_ID = file.read()

URL = "https://www.googleapis.com/customsearch/v1"

APP_PORT = int(os.getenv("APP_PORT", default="8000"))
IMAGE_SEARCH_MAX_RESULTS = int(os.getenv("IMAGE_SEARCH_MAX_RESULTS", default="3"))

app = FastAPI()


class SearchRequest(BaseModel):
    query: str

class Image(BaseModel):
    url: str

@app.post("/image-search", response_model=List[Image])
def post_search_google_images(request: SearchRequest):
    # Query parameters
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': request.query,
        'searchType': 'image',
        'num': IMAGE_SEARCH_MAX_RESULTS,
    }

    response = requests.get(URL, params=params)
    response.raise_for_status()

    results = response.json()
    print(str(results))

    if 'items' in results and len(results['items']) > 0:
        return [Image(url=str(item['link'])) for item in results['items']]
    else:
        print(f"No results found for '{request.query}'.")
        return None


@app.get("/image-search")
def get_search_google_images(query: str = Query(..., description="Search Google Images")):
    found_link = post_search_google_images(SearchRequest(query=query))
    return Response(content=f"<html><body><img src=\"{found_link}\"</body></html>", media_type="text/html")


@app.get("/health")
def get_health():
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
