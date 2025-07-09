FROM python:3.12-slim-bookworm

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY app/ app/

ARG APP_PORT_ARG=8000
ENV APP_PORT=${APP_PORT_ARG}
EXPOSE ${APP_PORT}

CMD ["python3", "-m", "app.main"]