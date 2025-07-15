from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.database.orm_models.base_orm import Base
import enum

from app.utils.constants import INCOME, EXPENSE, CARD, CASH

class TransactionType(enum.Enum):
    EXPENSE = EXPENSE
    INCOME  = INCOME
class PaymentMethod(enum.Enum):
    CARD = CARD
    CASH = CASH


class TransactionORM(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    amount = Column(Float, default=0.0)
    date = Column(DateTime, default=func.now())
    account_id = Column(String, nullable=False)
    type = Column(
        Enum(TransactionType, name="transaction_type"),
        default=TransactionType.EXPENSE,
        nullable=False
    )
    mcc_code = Column(Integer, default=0)
    currency_code = Column(Integer, default=980)
    description = Column(String, default="No description")
    payment_method = Column(
        Enum(PaymentMethod, name="payment_method"),
        default=PaymentMethod.CARD,
        nullable=False
    )
    cashback = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    is_synced = Column(Boolean, default=False)
