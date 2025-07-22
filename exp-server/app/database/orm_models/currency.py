from sqlalchemy import Column, BigInteger, String
from app.database.db import Base

class Currency(Base):
    __tablename__ = "currencies"
    currency_code = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "currency_code": self.currency_code,
            "name": self.name
        }