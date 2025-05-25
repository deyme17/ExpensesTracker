from server.database.db import SessionLocal
from server.models.currency import Currency

class CurrencyRepository:
    def get_all(self):
        with SessionLocal() as db:
            return [c.to_dict() for c in db.query(Currency).all()]