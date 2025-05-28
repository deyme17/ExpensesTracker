FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY run_api.py ./
COPY server/ ./server

EXPOSE 5000

CMD ["python", "run_api.py"]
