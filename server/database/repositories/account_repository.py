from server.database.db import SessionLocal
from server.models.account import Account

class AccountRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, data: dict):
        account = Account(**data)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
