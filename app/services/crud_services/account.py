import requests
from app.models.account import Account
import os
from dotenv import load_dotenv
from app.services.api import get_auth_headers, safe_request
from app.utils.error_codes import ErrorCodes

load_dotenv()
API_BASE = os.getenv("API_BASE")

class AccountService:
    def __init__(self, storage_service, user_id=None):
        self.storage_service = storage_service
        self.user_id = user_id

    def get_accounts(self):
        # local
        try:
            accounts = self.storage_service.get_accounts()

            if accounts:
                return accounts, None
            
        except Exception:
            pass

        # api
        if self.user_id:
            try:
                url = f"{API_BASE}/api/accounts/{self.user_id}"
                result = safe_request("GET", url, headers=get_auth_headers())

                if result.get("success"):
                    accounts = [Account.from_dict(acc) for acc in result["data"]]

                    if self.storage_service:
                        self.storage_service.save_accounts(accounts)
                    
                    return accounts, None
                
                else:
                    return [], result.get("error", ErrorCodes.UNKNOWN_ERROR)
                
            except Exception:
                return [], ErrorCodes.UNKNOWN_ERROR

        return [], ErrorCodes.OFFLINE_MODE