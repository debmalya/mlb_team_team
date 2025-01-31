FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip freeze


COPY . .
COPY data/ /app/data/  
COPY templates /app/templates
COPY gunicorn.conf.py gunicorn.conf.py


CMD ["python", "app.py"]
# CMD sh -c "gunicorn --bind 0.0.0.0:$PORT app:app -c ./gunicorn.conf.py"
