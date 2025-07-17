from sqlalchemy.orm import Session
from server.utils.encryption import Encryption as enc


class AccountSyncService:
    """
    Service responsible for synchronizing account data with the bank provider (e.g., MonoBank).
    Args:
        bank_service_cls: Class used to create a bank service instance (e.g., MonoBankService).
        account_service: Service responsible for local account CRUD operations.
        user_service: Service responsible for user-related operations.
    """

    def __init__(self, bank_service_cls, account_service, user_service):
        self.bank_service_cls = bank_service_cls
        self.account_service = account_service
        self.user_service = user_service

    def sync_account_by_id(self, user_id: str, account_id: str, db: Session = None):
        """
        Ensures that the specified account exists in the local database.
        If it doesn't, fetches client info from the bank API and tries to create the account.
        Args:
            user_id: ID of the user whose token will be used to access the bank API.
            account_id: ID of the account to synchronize.
            db: Optional session to use for DB operations.
        Returns:
            The account instance from the database (new or existing).
        """
        account = self.account_service.get_by_id(account_id, db)
        if account:
            return account
        
        bank = self._create_bank_instance(user_id, db)

        client_info = bank.get_client_info()
        for acc_data in client_info["accounts"]:
            if acc_data["id"] == account_id:
                new_account = {
                    "account_id": acc_data["id"],
                    "user_id": client_info["user_id"],
                    "currency_code": acc_data["currencyCode"],
                    "balance": acc_data["balance"] / 100.0,
                    "type": acc_data.get("type", "default"),
                    "masked_pan": acc_data.get("maskedPan", [None])[0]
                }
                return self.account_service.create(new_account, db)

        raise Exception(f"Account with id {account_id} not found in client-info response")
    
    def _create_bank_instance(self, user_id: str, db: Session = None):
        """
        Creates a bank service instance using the decrypted token of the specified user.
        Args:
            user_id: ID of the user whose token will be used to access the bank API.
            db: Optional session to use for DB operations.
        Returns:
            An instance of the external bank service (BankService).
        """
        user = self.user_service.get_by_id(user_id, db)
        if not user or not user.token:
            raise Exception(f"User {user_id} not found or token missing")
        
        decrypted_token = enc.decrypt(str(user.token))
        bank = self.bank_service_cls(decrypted_token)

        return bank
