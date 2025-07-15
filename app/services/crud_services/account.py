from app.api import get_auth_headers, safe_request, API_BASE
from app.utils.error_codes import ErrorCodes
from app.models.account import Account


class AccountService:
    """
    Handles account data retrieval from local storage or API.
    Args:
        local_storage: Service for local account storage operations
        user_id: Optional user identifier for API requests
    """
    def __init__(self, local_storage, user_id=None):
        self.local_storage = local_storage
        self.user_id = user_id

    def get_accounts(self) -> tuple[list, str]:
        """
        Retrieves accounts from local storage or API.
        Returns:
            Tuple: (list_of_accounts, error_message) 
                   Prioritizes local storage, falls back to API when needed
        """
        # local
        try:
            accounts = self.local_storage.accounts.get_accounts()
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

                    if self.local_storage:
                        self.local_storage.accounts.save_accounts(accounts)
                    
                    return accounts, None
                
                else:
                    return [], result.get("error", ErrorCodes.UNKNOWN_ERROR)
                
            except Exception:
                return [], ErrorCodes.UNKNOWN_ERROR

        return [], ErrorCodes.OFFLINE_MODE