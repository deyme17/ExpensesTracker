from server.database.db import SessionLocal
from server.models.transaction import Transaction
from sqlalchemy.exc import SQLAlchemyError


class TransactionRepository:
    def get_all_by_user(self, user_id: str):
        with SessionLocal() as db:
            return db.query(Transaction).filter(Transaction.user_id == user_id).all()

    def create_transaction(self, data: dict):
        with SessionLocal() as db:
            try:
                transaction = Transaction(**data)
                db.add(transaction)
                db.commit()
                db.refresh(transaction)
                return transaction
            except Exception as e:
                db.rollback()
                raise e

    def update(self, transaction_id: str, data: dict):
        with SessionLocal() as db:
            try:
                transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
                if not transaction:
                    raise Exception("Transaction not found")

                for key, value in data.items():
                    if hasattr(transaction, key):
                        setattr(transaction, key, value)

                db.commit()
                db.refresh(transaction)
                return transaction
            except Exception as e:
                db.rollback()
                raise e

    def delete(self, transaction_id: str):
        with SessionLocal() as db:
            try:
                transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
                if not transaction:
                    raise Exception("Transaction not found")

                db.delete(transaction)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e

    def get_by_id(self, transaction_id: str):
        with SessionLocal() as db:
            return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()