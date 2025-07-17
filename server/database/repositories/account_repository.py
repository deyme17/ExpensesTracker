from server.database.repositories.base_repository import BaseRepository
from server.database.orm_models.account import Account
from sqlalchemy.orm import Session


class AccountRepository(BaseRepository[Account]):
    def __init__(self):
        super().__init__(Account)

    def update_balance(self, account_id: str, val: float, db: Session = None) -> Account | None:
        with self.get_session(db) as session:
            account = session.query(Account).filter(Account.account_id == account_id).first()
            if not account:
                return None
            account.balance += val
            session.commit()
            session.refresh(account)
            return account
    
    def get_by_user_id(self, user_id: str, db: Session = None):
        with self.get_session(db) as session:
            return session.query(Account).filter(Account.user_id == user_id).all()

    def bulk_create(self, accounts_data: list, user_id: str, db: Session = None):
        with self.get_session(db) as session:
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
            session.add_all(accounts)
            session.flush()
            return accounts