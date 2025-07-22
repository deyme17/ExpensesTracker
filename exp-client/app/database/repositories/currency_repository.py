from sqlalchemy.orm import Session

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.currency import CurrencyORM
from app.models.currency import Currency


class CurrencyRepository(BaseRepository[CurrencyORM]):
    def __init__(self, session: Session):
        super().__init__(session, CurrencyORM)

    def save_currencies(self, currencies: list[Currency]) -> None:
        if not currencies:
            return None
        for cat in currencies:
            orm = CurrencyORM(
                currency_code=cat.currency_code,
                name=cat.name    
            )
            self.session.merge(orm)
        self.session.commit()

    def get_currencies(self) -> list[Currency]:
        orm_currencies = self.session.query(CurrencyORM).all()
        currencies = [Currency(
                currency_code=cat.currency_code,
                name=cat.name    
            ) for cat in orm_currencies]
        return currencies