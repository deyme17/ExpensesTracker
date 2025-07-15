from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.account import AccountORM
from app.models.account import Account


class AccountRepository(BaseRepository[AccountORM]):
    def __init__(self, session: Session):
        super().__init__(session, AccountORM)