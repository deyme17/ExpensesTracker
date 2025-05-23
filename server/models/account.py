from sqlalchemy import Column, String, BigInteger, ForeignKey, DECIMAL, VARCHAR
from server.database.db import Base

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    currency_code = Column(BigInteger, ForeignKey("currencies.currency_code"), nullable=False)
    balance = Column(DECIMAL(19, 4), nullable=False)
    type = Column(VARCHAR(255), nullable=False)
    masked_pan = Column(BigInteger, nullable=False)