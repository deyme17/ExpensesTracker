from server.database.db import SessionLocal
from server.models.transaction import Transaction

class TransactionRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create_transaction(self, data: dict):
        try:
            transaction = Transaction(**data)
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        except Exception as e:
            self.db.rollback()
            raise e
