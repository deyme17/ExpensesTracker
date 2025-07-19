FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY expenses-tracker-client/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY expenses-tracker-client/ ./

CMD ["python", "main.py"]
