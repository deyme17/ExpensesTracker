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
        
    def bulk_create(self, accounts_data: list, user_id: str, db):
        accounts = [
            Account(
                account_id=a["id"],
                user_id=user_id,
                currency_code=a["currencyCode"],
                balance=a["balance"] / 100.0,
                type=a.get("type", "default"),
                masked_pan=a.get("maskedPan", [None])[0]
            )
            for a in accounts_data
        ]
        for acc in accounts:
            db.add(acc)
        db.flush()
        return accounts
