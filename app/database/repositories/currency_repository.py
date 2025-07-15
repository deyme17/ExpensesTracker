from sqlalchemy.orm import Session
from typing import Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.currency import CurrencyORM
from app.models.currency import Currency


class CurrencyRepository(BaseRepository[CurrencyORM]):
    def __init__(self, session: Session):
        super().__init__(session, CurrencyORM)