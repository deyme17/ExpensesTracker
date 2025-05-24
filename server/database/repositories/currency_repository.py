from server.database.db import SessionLocal
from server.models.currency import Currency

class CurrencyRepository:
    def get_all(self):
        with SessionLocal() as db:
            return db.query(Currency).all()