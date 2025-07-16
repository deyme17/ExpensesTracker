from .base_webhook_service import BaseWebHookService


class MonoWebHookService(BaseWebHookService):
    """
    Handles webhook data from MonoBank and saves transactions.
    Args:
        transaction_service: Service for CRUD transaction operations (is used for transaction saving)
        account_service: Service for CRUD account operations (is used for balance updates)
    """
    def __init__(self,transaction_service, account_service):
        self.transaction_service = transaction_service
        self.account_service = account_service

    def save_hooked_transactions(self, data: dict) -> None:
        transactions = data.get("transactions", [])
        if not transactions:
            raise ValueError("No transactions found in webhook payload")

        for tx in transactions:
            self._save_transaction(tx)

    def _save_transaction(self, tx_data: dict) -> None:
        """
        Saves a single transaction and updates the account balance.
        """
        transaction = self.transaction_service.create(tx_data)
        self.account_service.update_balance(
            account_id=transaction.account_id,
            amount=transaction.amount,
        )
