from sqlalchemy.orm import Session


class AccountSyncService:
    def __init__(self, bank_service, account_service):
        self.bank_service = bank_service
        self.account_service = account_service

    def sync_account_by_id(self, account_id: str, db: Session = None):
        """
        Ensures the given account_id exists in DB.
        If not, tries to fetch account info from MonoBank and create it.
        """
        account = self.account_service.get_by_id(account_id, db)
        if account:
            return account

        client_info = self.bank_service.get_client_info()
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
