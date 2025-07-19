from .base_webhook_service import BaseWebHookService
from sqlalchemy.orm import Session
from datetime import datetime as dt


class MonoWebHookService(BaseWebHookService):
    """Handles webhook data from Monobank and saves transactions.
    Args:
        transaction_service: Service for transaction CRUD operations
        account_service: Service for account operations
        user_service: Service for user data retrieval
    """
    def __init__(self, transaction_service, account_service, user_service):
        self.transaction_service = transaction_service
        self.account_service = account_service
        self.user_service = user_service

    def save_hooked_transactions(self, data: dict, db: Session = None) -> None:
        """
        Entry point to process webhook payload.
        Args:
            data: Raw webhook payload from Monobank
            db: Optional database session
        """
        statement, account_id = self._extract_valid_statement(data)
        if not statement or not account_id:
            return

        tx_data = self._build_transaction_data(statement, account_id, db)
        self._save_transaction(tx_data, db)

    def _extract_valid_statement(self, data: dict) -> tuple[dict, str]:
        """
        Validates webhook payload structure and extracts needed fields.
        Args:
            data: Raw webhook payload
        Returns:
            Tuple containing webhook statement and id of account
        """
        hook_type = data.get("type")
        if hook_type != "StatementItem":
            print(f"[Webhook] Unsupported type: {hook_type}")
            return None, None

        hook_data = data.get("data", {})
        statement = hook_data.get("statementItem")
        account_id = hook_data.get("account")

        if not statement or not account_id:
            print(f"[Webhook] Invalid payload. account_id={account_id}, statement={statement}")
            return None, None

        return statement, account_id

    def _build_transaction_data(self, statement: dict, account_id: str, db: Session) -> dict:
        """
        Builds transaction data from statement.
        Args:
            statement: Processed statement item from webhook
            account_id: Target account identifier
            db: Optional database session
        Returns:
            Dictionary with transaction data
        """
        return {
            "id": statement["id"],
            "account": account_id,
            "amount": statement["amount"] / 100.0,
            "mcc_code": statement["mcc"],
            "currency_code": statement["currencyCode"],
            "description": statement.get("description", "without_description"),
            "cashback": statement.get("cashbackAmount", 0) / 100.0,
            "commission": (statement.get("commissionRate", 0) * abs(statement["amount"]) / 10000) / 100.0,
            "date": dt.utcfromtimestamp(statement["time"]).date(),
            "user_id": self.user_service.get_user_by_account_id(account_id, db),
            "payment_method": "card",
        }

    def _save_transaction(self, tx_data: dict, db: Session = None) -> None:
        """
        Saves a single transaction and updates the account balance.
        Args:
            tx_data: Prepared transaction data
            db: Optional database session
        """
        if not self._validate_hooking(tx_data, db):
            return

        transaction = self.transaction_service.create(tx_data, db)
        self.account_service.update_balance(
            account_id=transaction.account_id,
            amount=transaction.amount,
            db=db
        )

    def _validate_hooking(self, tx_data: dict, db: Session = None) -> bool:
        """
        Validates whether a transaction can be saved.
        Args:
            tx_data: Transaction data to validate
            db: Optional database session
        Returns:
            bool: True if transaction should be processed
        """
        account = self.account_service.get_by_id(tx_data["account"], db)
        if not account:
            print(f"[Webhook] Skipping: account {tx_data['account']} not found")
            return False

        if self.transaction_service.get_by_id(tx_data["id"], db):
            print(f"[Webhook] Skipping: transaction {tx_data['id']} already exists")
            return False

        return True