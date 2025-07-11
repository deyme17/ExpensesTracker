import requests
from app.utils.token_exp import is_token_expired
from app.utils.error_codes import ErrorCodes

import os
from dotenv import load_dotenv
load_dotenv()
API_BASE = os.getenv("API_BASE")

def get_auth_headers():
    try:
        from app.services.local_storage import LocalStorageService
        user = LocalStorageService().get_user()

        if user and user.token:
            if is_token_expired(user.token):
                print("[API] Token expired, need to re-login")
                return {}
            return {"Authorization": f"Bearer {user.token}"}
        
    except Exception:
        pass
    return {}

def safe_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=5, **kwargs)

        if response.status_code == 429:
            return {"success": False, "error": ErrorCodes.TOO_MANY_REQUESTS}
        
        if not response.ok:
            return {"success": False, "error": ErrorCodes.SERVER_UNREACHABLE}
        
        return response.json()
    
    except requests.ConnectionError:
        return {"success": False, "error": ErrorCodes.SERVER_UNREACHABLE}
    
    except requests.Timeout:
        return {"success": False, "error": ErrorCodes.TIMEOUT}
    
    except Exception:
        return {"success": False, "error": ErrorCodes.UNKNOWN_ERROR}

def api_get_transactions(user_id):
    return safe_request("GET", f"{API_BASE}/api/transactions/{user_id}", 
                        headers=get_auth_headers())

def api_add_transaction(data):
    return safe_request("POST", f"{API_BASE}/api/transaction", 
                        json=data, headers=get_auth_headers())

def api_get_transaction_by_id(transaction_id):
    return safe_request("GET", f"{API_BASE}/api/transaction/{transaction_id}", 
                        headers=get_auth_headers())

def api_delete_transaction(transaction_id):
    return safe_request("DELETE", f"{API_BASE}/api/transaction/{transaction_id}", 
                        headers=get_auth_headers())

def api_update_transaction(transaction_id, data):
    return safe_request("PATCH", f"{API_BASE}/api/transaction/{transaction_id}", 
                        json=data, headers=get_auth_headers())

def api_get_categories():
    return safe_request("GET", f"{API_BASE}/api/categories", 
                        headers=get_auth_headers())

def api_get_currencies():
    return safe_request("GET", f"{API_BASE}/api/currencies", 
                        headers=get_auth_headers())

def api_register(payload):
    return safe_request("POST", f"{API_BASE}/api/auth/register", 
                        json=payload)

def api_login(payload):
    return safe_request("POST", f"{API_BASE}/api/auth/login", 
                        json=payload)
