FROM python:3.12-slim-bookworm

RUN apt-get update -y && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

ENV APP_PORT=8000
ENV ANKI_CONNECT_URL=http://host.docker.internal:8765
ENV STORAGE_MODE=ANKI

EXPOSE $APP_PORT

# Run uvicorn server. Use sh -c to expand the environment variable.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $APP_PORT"]