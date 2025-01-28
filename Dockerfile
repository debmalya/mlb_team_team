FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=1000:1000 . . 

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
