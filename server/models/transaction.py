from sqlalchemy import Column, BigInteger, String, DECIMAL, Date, ForeignKey
from server.database.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    account_id = Column(String, ForeignKey("accounts.account_id"), nullable=False)
    amount = Column(DECIMAL(19, 4), nullable=False)
    date = Column(Date, nullable=False)
    currency_code = Column(BigInteger, ForeignKey("currency.currency_code"), nullable=False)
    mcc_code = Column(BigInteger, ForeignKey("category.mcc_code"), nullable=False)
    type = Column(String(255), nullable=False, default="card")
    description = Column(String(255), nullable=False, default="Без опису")
    cashback = Column(DECIMAL(19, 4), nullable=False, default=0)
    commission = Column(DECIMAL(19, 4), nullable=False, default=0)

