# server/models/transaction.py
from sqlalchemy import Column, String, Date, DECIMAL, ForeignKey, BigInteger
from server.database.db import Base
from server.models.category import Category
class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    amount = Column(DECIMAL(19, 4), nullable=False)
    date = Column(Date)
    currency_code = Column(BigInteger, default=980)
    mcc_code = Column(BigInteger, ForeignKey("category.mcc_code"), default=0)
    type = Column(String, default='card')
    description = Column(String, default='Without_description')
    cashback = Column(DECIMAL(19,4), default=0)
    commission = Column(DECIMAL(19,4), default=0)
