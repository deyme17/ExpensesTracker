from sqlalchemy.orm import Session
from typing import Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.account import AccountORM
from app.models.account import Account


class AccountRepository(BaseRepository[AccountORM]):
    def __init__(self, session: Session):
        super().__init__(session, AccountORM)

    def save_accounts(self, accounts: list[Account]) -> None:
        if not accounts:
            return None
        for acc in accounts:
            orm = AccountORM(
                account_id=acc.account_id,
                user_id=acc.user_id,
                type=acc.type,
                currency_code=acc.currency_code,
                balance=acc.balance,
                masked_pan=acc.masked_pan          
            )
            self.session.merge(orm)
        self.session.commit()

    def get_accounts_by_id(self, user_id: str) -> list[Account]:
        orm_accounts = self.session.query(AccountORM).filter_by(user_id=user_id).all()
        accounts = [Account(
                        account_id=acc.account_id,
                        user_id=acc.user_id,
                        type=acc.type,
                        currency_code=acc.currency_code,
                        balance=acc.balance,
                        masked_pan=acc.masked_pan          
                    ) for acc in orm_accounts]
        return accounts
    
    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        orm = self.get_by_id(account_id)
        if orm:
            return Account(
                account_id=orm.account_id,
                user_id=orm.user_id,
                type=orm.type,
                currency_code=orm.currency_code,
                balance=orm.balance,
                masked_pan=orm.masked_pan
            )
        return None