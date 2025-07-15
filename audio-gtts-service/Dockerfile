FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_PORT=8000
EXPOSE $APP_PORT

CMD ["python", "audio.py"]
