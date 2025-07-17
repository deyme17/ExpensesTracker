from .base_webhook_service import BaseWebHookService
from sqlalchemy.orm import Session


class MonoWebHookService(BaseWebHookService):
    """
    Handles webhook data from MonoBank and saves transactions.
    Args:
        transaction_service: Service for CRUD transaction operations (is used for transaction saving)
        account_service: Service for CRUD account operations (is used for balance updates)
         account_sync_service: Service to ensure accounts exist and are synced from Monobank API
    """
    def __init__(self, transaction_service, account_service, account_sync_service):
        self.transaction_service = transaction_service
        self.account_service = account_service
        self.account_sync_service = account_sync_service

    def save_hooked_transactions(self, data: dict, db: Session = None) -> None:
        """
        Extracts and saves all transactions from a webhook payload.
        Args:
            data: The webhook payload containing transaction data.
            db: Optional database session
        """
        transactions = data.get("transactions", [])
        if not transactions:
            raise ValueError("No transactions found in webhook payload")

        for tx in transactions:
            self._save_transaction(tx, db)

    def _save_transaction(self, tx_data: dict, db: Session = None) -> None:
        """
        Saves a single transaction and updates the account balance.
        """
        self.account_sync_service.sync_account_by_id(tx_data["account"], db)

        transaction = self.transaction_service.create(tx_data, db)
        self.account_service.update_balance(
            account_id=transaction.account_id,
            amount=transaction.amount,
            db=db
        )
