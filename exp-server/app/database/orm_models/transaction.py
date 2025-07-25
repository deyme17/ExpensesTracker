from sqlalchemy import Column, BigInteger, String, DECIMAL, Date, ForeignKey, Enum, Computed
from app.database.db import Base
from sqlalchemy import text
import enum

class PaymentMethod(enum.Enum):
    card = "card"
    cash = "cash"

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    amount = Column(DECIMAL(19, 4), nullable=False)
    date = Column(Date, nullable=False)
    account_id = Column(String, ForeignKey("accounts.account_id"), nullable=False)
    mcc_code = Column(BigInteger, ForeignKey("categories.mcc_code"), nullable=False)
    currency_code = Column(BigInteger, ForeignKey("currencies.currency_code"), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False, default=PaymentMethod.card)
    type = Column(String(10), Computed("CASE WHEN amount > 0 THEN 'income' WHEN amount < 0 THEN 'expense' ELSE 'zero' END", persisted=True))
    description = Column(String(255), nullable=False, default="without_description")
    cashback = Column(DECIMAL(19, 4), nullable=False, default=0)
    commission = Column(DECIMAL(19, 4), nullable=False, default=0)

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": float(self.amount),
            "date": self.date.isoformat() if self.date else None,
            "account_id": self.account_id,
            "mcc_code": int(self.mcc_code),
            "currency_code": int(self.currency_code),
            "payment_method": self.payment_method.value,
            "type": self.type,
            "description": self.description,
            "cashback": float(self.cashback),
            "commission": float(self.commission),
        }