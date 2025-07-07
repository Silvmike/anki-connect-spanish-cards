FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV APP_PORT=8000
EXPOSE $APP_PORT

CMD ["python", "translate.py"]