from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Enum
from sqlalchemy.sql import func
import enum

from app.database.orm_models.base_orm import Base
from app.utils.constants import CARD, DEFAULT_CURRENCY_CODE, DEFAULT_MCC


class TransactionORM(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    amount = Column(Float, default=0.0)
    date = Column(DateTime, default=func.now())
    account_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    mcc_code = Column(Integer, default=DEFAULT_MCC)
    currency_code = Column(Integer, default=DEFAULT_CURRENCY_CODE)
    description = Column(String, default="No description")
    payment_method = Column(String, nullable=False, default=CARD)
    cashback = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    is_synced = Column(Boolean, default=False)
