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
    def __init__(self):
        self.repo = TransactionRepository()

    def get_all_by_user(self, user_id):
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

    def create(self, data):
        return self.repo.create(data)

    def delete(self, transaction_id):
        return self.repo.delete(transaction_id)

    def update(self, transaction_id, data):
        return self.repo.update(transaction_id, data)
    
    def map_transactions(self, tx_data, user_id, account_id):
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


transaction_service = TransactionService()