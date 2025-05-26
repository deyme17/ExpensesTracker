import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE")


def get_auth_headers():
    try:
        from app.services.local_storage import LocalStorageService
        user = LocalStorageService().get_user()
        if user and user.token:
            return {"Authorization": f"Bearer {user.token}"}
    except Exception:
        pass
    return {}


def api_get_transactions(user_id):
    return requests.get(
        f"{API_BASE}/api/transactions/{user_id}",
        headers=get_auth_headers()
    ).json()


def api_add_transaction(data):
    return requests.post(
        f"{API_BASE}/api/transaction",
        json=data,
        headers=get_auth_headers()
    ).json()


def api_get_transaction_by_id(transaction_id):
    try:
        response = requests.get(f"{API_BASE}/api/transaction/{transaction_id}")
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}


def api_delete_transaction(transaction_id):
    return requests.delete(
        f"{API_BASE}/api/transaction/{transaction_id}",
        headers=get_auth_headers()
    ).json()


def api_update_transaction(transaction_id, data):
    return requests.patch(
        f"{API_BASE}/api/transaction/{transaction_id}",
        json=data,
        headers=get_auth_headers()
    ).json()


def api_get_categories():
    return requests.get(
        f"{API_BASE}/api/categories",
        headers=get_auth_headers()
    ).json()


def api_get_currencies():
    return requests.get(
        f"{API_BASE}/api/currencies",
        headers=get_auth_headers()
    ).json()


def api_register(payload):
    try:
        response = requests.post(f"{API_BASE}/api/auth/register", json=payload)
        if response.status_code != 200:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}


def api_login(payload):
    try:
        response = requests.post(f"{API_BASE}/api/auth/login", json=payload)
        if response.status_code != 200:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}