from app.api import get_auth_headers, safe_request, API_BASE
from app.utils.error_codes import ErrorCodes
from app.models.user import User


class AccountService:
    """
    Handles account data retrieval from local storage or API.
    Args:
        storage_service: Service for local account storage operations
        user_id: Optional user identifier for API requests
    """
    def __init__(self, storage_service, user_id=None):
        self.storage_service = storage_service
        self.user_id = user_id

    def get_accounts(self):
        """
        Retrieves accounts from local storage or API.
        Returns:
            Tuple: (list_of_accounts, error_message) 
                   Prioritizes local storage, falls back to API when needed
        """
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
                    accounts = [User.from_dict(acc) for acc in result["data"]]

                    if self.storage_service:
                        self.storage_service.save_accounts(accounts)
                    
                    return accounts, None
                
                else:
                    return [], result.get("error", ErrorCodes.UNKNOWN_ERROR)
                
            except Exception:
                return [], ErrorCodes.UNKNOWN_ERROR

        return [], ErrorCodes.OFFLINE_MODE