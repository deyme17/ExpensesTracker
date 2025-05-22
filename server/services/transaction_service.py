from server.database.repositories.transaction_repository import TransactionRepository
from server.models.transaction import Transaction

class TransactionService:
    def __init__(self):
        self.repo = TransactionRepository()

    def create_transaction(self, data):
        return self.repo.create_transaction(data)
