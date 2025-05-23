import requests

API_BASE = "http://localhost:5000/api"

def send_transaction(transaction_data):
    response = requests.post(f"{API_BASE}/transactions", json=transaction_data)
    return response.json()
