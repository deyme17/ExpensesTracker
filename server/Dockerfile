FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY server/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./

ENV FLASK_APP=main.py

CMD ["python", "main.py"]
