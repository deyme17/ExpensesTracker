from server.database.repositories.transaction_repository import TransactionRepository
import enum
from datetime import date, datetime
from decimal import Decimal

def serialize(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, enum.Enum):
        return obj.value
    return str(obj)


class TransactionService:
    """
    Service layer for transaction operations.
    Args:
        repository: TransactionRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def get_all_by_user(self, user_id: str) -> list[dict]:
        """
        Retrieves all transactions for specified user.
        Args:
            user_id: User's unique identifier
        Returns:
            List of transaction dictionaries with serialized values
        """
        transactions = self.repo.get_all_by_user(user_id)
        return [
            {
                "transaction_id": t.transaction_id,
                "user_id": t.user_id,
                "amount": float(t.amount),
                "date": t.date.isoformat(),
                "account_id": t.account_id,
                "mcc_code": t.mcc_code,
                "currency_code": t.currency_code,
                "payment_method": t.payment_method.value if t.payment_method else "card",
                "type": t.type,
                "description": t.description,
                "cashback": float(t.cashback),
                "commission": float(t.commission)
            }
            for t in transactions
        ]

    def create(self, data: dict):
        """
        Creates new transaction.
        Args:
            data: Transaction data dictionary
        Returns:
            Created transaction object
        """
        return self.repo.create(data)

    def delete(self, transaction_id: str) -> None:
        """
        Deletes specified transaction.
        Args:
            transaction_id: Transaction's unique identifier
        """
        return self.repo.delete(transaction_id)

    def update(self, transaction_id: str, data: dict):
        """
        Updates existing transaction.
        Args:
            transaction_id: Transaction's unique identifier
            data: Updated transaction data
        Returns:
            Updated transaction object
        """
        return self.repo.update(transaction_id, data)
    
    def map_transactions(self, tx_data: list[dict], user_id: str, account_id: str) -> list:
        """
        Maps external transaction data to ORM models.
        Args:
            tx_data: List of raw transaction dictionaries
            user_id: Associated user ID
            account_id: Associated account ID
        Returns:
            List of Transaction ORM objects
        """
        from server.database.orm_models.transaction import Transaction
        return [
            Transaction(
                transaction_id=t["id"],
                user_id=user_id,
                amount=t["amount"] / 100.0,
                date=datetime.fromtimestamp(t["time"]),
                account_id=account_id,
                mcc_code=t.get("mcc", 0),
                currency_code=t.get("currencyCode", 980),
                payment_method="card",
                description=t.get("description", ""),
                cashback=t.get("cashbackAmount", 0) / 100.0,
                commission=t.get("commissionRate", 0) / 100.0
            )
            for t in tx_data
        ]


transaction_service = TransactionService(repository=TransactionRepository())