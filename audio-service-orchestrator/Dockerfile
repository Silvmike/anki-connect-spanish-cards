FROM python:3.12-slim-bookworm

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy the application
COPY . .

ENV PYTHONPATH=/app

ARG AUDIO_SERVICE_HOST=audio-service
ARG AUDIO_SERVICE_PORT=8000
ARG AUDIO_UPLOAD_SERVICE_HOST=yandex-disk-service
ARG AUDIO_UPLOAD_SERVICE_PORT=8000

ENV AUDIO_SERVICE_HOST=$AUDIO_SERVICE_HOST
ENV AUDIO_SERVICE_PORT=$AUDIO_SERVICE_PORT

ENV AUDIO_UPLOAD_SERVICE_HOST=$AUDIO_UPLOAD_SERVICE_HOST
ENV AUDIO_UPLOAD_SERVICE_PORT=$AUDIO_UPLOAD_SERVICE_PORT

ARG APP_PORT_ARG=8000
ENV APP_PORT=$APP_PORT_ARG
EXPOSE $APP_PORT

CMD ["python", "-m", "app.main"]