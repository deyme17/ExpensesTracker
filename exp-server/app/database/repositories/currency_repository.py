from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.currency import Currency


class CurrencyRepository(BaseRepository[Currency]):
    def __init__(self):
        super().__init__(Currency)