FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip freeze


COPY . .
COPY data/2024.json /app/data/  
COPY templates /app/templates


CMD ["python", "app.py"]
