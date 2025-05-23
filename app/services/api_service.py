import requests

API_BASE = "http://localhost:5000/api"

def api_register(data):
    response = requests.post(f"{API_BASE}/register", json=data)
    return response.json()

def api_login(data):
    response = requests.post(f"{API_BASE}/login", json=data)
    return response.json()