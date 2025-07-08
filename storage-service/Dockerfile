FROM python:3.12-slim-bookworm

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pydantic-settings

WORKDIR /app
COPY . .

ENV APP_PORT=8000
EXPOSE $APP_PORT

ENV PYTHONPATH=/app

CMD ["python3", "-m", "main.py"]