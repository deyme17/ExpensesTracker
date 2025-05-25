from server.database.repositories.transaction_repository import TransactionRepository
import enum
from datetime import date, datetime
from decimal import Decimal
import json

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
        return [json.loads(json.dumps(t.__dict__, default=serialize)) for t in transactions]


    def create(self, data):
        return self.repo.create_transaction(data)

    def delete(self, transaction_id):
        return self.repo.delete(transaction_id)

    def update(self, transaction_id, data):
        return self.repo.update(transaction_id, data)

transaction_service = TransactionService()