from server.database.db import SessionLocal
from server.models.currency import Currency

class CurrencyRepository:
    def get_all(self):
        try:
            with SessionLocal() as db:
                currencies = db.query(Currency).all()
                return currencies
        except Exception as e:
            print(f"[CurrencyRepository] Error querying currencies: {str(e)}")
            raise