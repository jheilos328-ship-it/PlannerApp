FROM python:3.12-slim

WORKDIR /app

COPY V4/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY V4/ .

ENV PORT=8080

CMD gunicorn --bind 0.0.0.0:${PORT} serverway2clean:app
