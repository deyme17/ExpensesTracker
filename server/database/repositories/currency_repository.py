from server.database.db import SessionLocal
from server.models.currency import Currency

class CurrencyRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        return self.db.query(Currency).all()