FROM python:3.12-slim-bookworm

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

ENV APP_PORT=8000
EXPOSE $APP_PORT

CMD ["python", "drive.py"]