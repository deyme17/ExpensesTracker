from sqlalchemy import Column, String, BigInteger, ForeignKey, DECIMAL, VARCHAR
from app.database.db import Base

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    currency_code = Column(BigInteger, ForeignKey("currencies.currency_code"), nullable=False)
    balance = Column(DECIMAL(19, 4), nullable=False)
    type = Column(VARCHAR(255), nullable=False)
    masked_pan = Column(String, nullable=True)

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "currency_code": self.currency_code,
            "balance": float(self.balance),
            "type": self.type,
            "masked_pan": self.masked_pan
        }