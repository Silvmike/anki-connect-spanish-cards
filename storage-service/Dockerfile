FROM python:3.11

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

ENV APP_PORT=8000
EXPOSE $APP_PORT

CMD ["python", "main.py"]