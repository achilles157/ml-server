FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY ml_models ./ml_models
EXPOSE $PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT