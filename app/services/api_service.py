import requests

API_BASE = "http://localhost:5000/api"

def api_get_transactions(user_id):
    response = requests.get(f"{API_BASE}/transactions/{user_id}")
    return response.json()

def api_add_transaction(data):
    return requests.post(f"{API_BASE}/transaction", json=data).json()

def api_delete_transaction(transaction_id):
    return requests.delete(f"{API_BASE}/transaction/{transaction_id}").json()

def api_update_transaction(transaction_id, data):
    return requests.patch(f"{API_BASE}/transaction/{transaction_id}", json=data).json()
