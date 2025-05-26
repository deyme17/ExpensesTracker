import requests
from app.models.account import Account
import os
from dotenv import load_dotenv
from app.services.api_service import get_auth_headers

load_dotenv()
API_BASE = os.getenv("API_BASE")


class AccountService:
    def __init__(self, storage_service, user_id=None):
        self.storage_service = storage_service
        self.user_id = user_id

    def get_accounts(self):
        try:
            accounts = self.storage_service.get_accounts()
            if accounts:
                return accounts
        except Exception:
            pass

        if self.user_id:
            try:
                response = requests.get(
                    f"{API_BASE}/api/accounts/{self.user_id}",
                    headers=get_auth_headers()
                )
                result = response.json()
                if result.get("success"):
                    accounts = [Account.from_dict(acc) for acc in result["data"]]
                    if self.storage_service:
                        self.storage_service.save_accounts(accounts)
                    return accounts
            except Exception as e:
                print(f"[AccountService] Remote fetch failed: {e}")

        return []