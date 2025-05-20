from server.database.db import SessionLocal
from server.models.transaction import Transaction

class TransactionRepository:
    def __init__(self):
        self.db = SessionLocal()

<<<<<<< HEAD
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
=======
    def get_all_by_user(self, user_id: str):
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()

    def create(self, data: dict):
        transaction = Transaction(**data)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete(self, transaction_id: int):
        transaction = self.db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
        if transaction:
            self.db.delete(transaction)
            self.db.commit()
            return True
        return False

    def update(self, transaction_id: int, data: dict):
        transaction = self.db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
        if transaction:
            for key, value in data.items():
                setattr(transaction, key, value)
            self.db.commit()
            return transaction
        raise Exception("Транзакція не знайдена")
>>>>>>> 9765729 (completed api)
