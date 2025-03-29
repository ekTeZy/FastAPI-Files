FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p static/audio

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
