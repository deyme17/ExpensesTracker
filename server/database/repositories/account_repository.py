from server.database.db import SessionLocal
from server.models.account import Account

class AccountRepository:
    def create(self, data: dict):
        with SessionLocal() as db:
            account = Account(**data)
            db.add(account)
            db.commit()
            db.refresh(account)
            return account

    def get_by_user_id(self, user_id):
        with SessionLocal() as db:
            return db.query(Account).filter(Account.user_id == user_id).all()