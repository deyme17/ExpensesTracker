from sqlalchemy.orm import Session
from typing import Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.transaction import TransactionORM
from app.models.transaction import Transaction


class TransactionRepository(BaseRepository[TransactionORM]):
    def __init__(self, session: Session):
        super().__init__(session, TransactionORM)