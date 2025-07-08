FROM python:3.11

RUN pip install coqui-tts --no-cache-dir
RUN pip install --no-cache-dir uvicorn fastapi pydantic

WORKDIR /app
COPY . .

ENV APP_PORT=8000
EXPOSE $APP_PORT

CMD ["python", "audio.py"]