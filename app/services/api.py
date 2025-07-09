import requests
import os
from dotenv import load_dotenv
from app.utils.error_codes import ErrorCodes

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")
API_BASE = os.getenv("API_BASE")

def get_auth_headers() -> dict:
    try:
        from app.services.local_storage import LocalStorageService
        user = LocalStorageService().get_user()

        if user and user.token:
            return {"Authorization": f"Bearer {user.token}"}
        
    except Exception:
        pass
    return {}

def safe_request(method: str, url: str, timeout: int = 15, **kwargs) -> dict:
    try:
        print(f"[REQUEST] {method} {url}")
        response = requests.request(method, url, timeout=timeout, **kwargs)
        print(f"[RESPONSE] Status: {response.status_code}")
        print(f"[RESPONSE] Body: {response.text}")

        if response.status_code == 429:
            return {"success": False, "error": ErrorCodes.TOO_MANY_REQUESTS}

        try:
            data = response.json()
        except Exception as json_err:
            print(f"[ERROR] JSON decode failed: {json_err}")
            return {"success": False, "error": ErrorCodes.UNKNOWN_ERROR}

        return data

    except requests.Timeout:
        print("[ERROR] Request timed out")
        return {"success": False, "error": ErrorCodes.TIMEOUT}

    except requests.ConnectionError:
        print("[ERROR] Server unreachable")
        return {"success": False, "error": ErrorCodes.SERVER_UNREACHABLE}

    except Exception as e:
        print(f"[ERROR] Unexpected: {str(e)}")
        return {"success": False, "error": ErrorCodes.UNKNOWN_ERROR}

def api_get_transactions(user_id: str) -> dict:
    return safe_request("GET", f"{API_BASE}/api/transactions/{user_id}", 
                        headers=get_auth_headers())

def api_add_transaction(data: dict) -> dict:
    return safe_request("POST", f"{API_BASE}/api/transaction", 
                        json=data, headers=get_auth_headers())

def api_get_transaction_by_id(transaction_id: str) -> dict:
    return safe_request("GET", f"{API_BASE}/api/transaction/{transaction_id}", 
                        headers=get_auth_headers())

def api_delete_transaction(transaction_id: str) -> dict:
    return safe_request("DELETE", f"{API_BASE}/api/transaction/{transaction_id}", 
                        headers=get_auth_headers())

def api_update_transaction(transaction_id: str, data) -> dict:
    return safe_request("PATCH", f"{API_BASE}/api/transaction/{transaction_id}", 
                        json=data, headers=get_auth_headers())

def api_get_categories() -> dict:
    return safe_request("GET", f"{API_BASE}/api/categories", 
                        headers=get_auth_headers())

def api_get_currencies() -> dict:
    return safe_request("GET", f"{API_BASE}/api/currencies", 
                        headers=get_auth_headers())

def api_register(payload: dict) -> dict:
    return safe_request("POST", f"{API_BASE}/api/auth/register", 
                        json=payload, timeout=25)

def api_login(payload: dict) -> dict:
    return safe_request("POST", f"{API_BASE}/api/auth/login", 
                        json=payload)
