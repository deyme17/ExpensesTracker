from .base_webhook_service import BaseWebHookService
from sqlalchemy.orm import Session


class MonoWebHookService(BaseWebHookService):
    """
    Handles webhook data from MonoBank and saves transactions.
    Args:
        transaction_service: Service for CRUD transaction operations (is used for transaction saving)
        account_service: Service for CRUD account operations (is used for balance updates)
    """
    def __init__(self, transaction_service, account_service):
        self.transaction_service = transaction_service
        self.account_service = account_service

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
        if not self._validate_hooking(tx_data, db):
            return

        transaction = self.transaction_service.create(tx_data, db)
        self.account_service.update_balance(
            account_id=transaction.account_id,
            amount=transaction.amount,
            db=db
        )

    def _validate_hooking(self, tx_data: dict, db: Session) -> bool:
        """
        Validates whether a transaction can be hooked/saved.
        Checks if the account exists and the transaction is not duplicated.
        """
        account = self.account_service.get_by_id(tx_data["account"], db)
        if not account:
            print(f"Skipping transaction: account {tx_data['account']} not found")
            return False

        existing = self.transaction_service.get_by_id(tx_data["id"], db)
        if existing:
            print(f"Transaction {tx_data['id']} already exists")
            return False

        return True
