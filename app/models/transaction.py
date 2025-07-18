from datetime import datetime
from app.utils.formatters import format_amount, format_date
from app.utils.constants import CARD, EXPENSE, DEFAULT_CURRENCY_CODE
from typing import Optional


class Transaction:
    def __init__(self, transaction_id: str, user_id: str, amount: str|int|float, date: datetime, account_id: str,
                 mcc_code: int|str, currency_code: int|str, description: str = "", payment_method: str = CARD, type: str = EXPENSE,
                 cashback: float|int|str = 0.0, commission: float|int|str = 0.0):

        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = float(amount)
        self.date = self._parse_date(date)
        self.account_id = account_id
        self.type = type
        self.mcc_code = int(mcc_code) if mcc_code is not None else 0
        self.currency_code = int(currency_code)
        self.description = description
        self.payment_method = payment_method
        self.cashback = float(cashback)
        self.commission = float(commission)

    def _parse_date(self, date: str) -> datetime:
        if isinstance(date, datetime):
            return date
        if isinstance(date, str):
            for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return datetime.strptime(date, fmt)
                except ValueError:
                    continue
        return datetime.now()

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "account_id": self.account_id,
            "type": self.type,
            "mcc_code": self.mcc_code,
            "currency_code": self.currency_code,
            "description": self.description,
            "payment_method": self.payment_method,
            "cashback": self.cashback,
            "commission": self.commission,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional['Transaction']:
        if not data:
            return None
        return cls(
            transaction_id=data.get("transaction_id"),
            user_id=data.get("user_id"),
            amount=data.get("amount", 0.0),
            date=data.get("date"),
            account_id=data.get("account_id"),
            type=data.get("type", EXPENSE),
            mcc_code=data.get("mcc_code", 0),
            currency_code=data.get("currency_code", DEFAULT_CURRENCY_CODE),
            description=data.get("description", ""),
            payment_method=data.get("payment_method", CARD),
            cashback=data.get("cashback", 0.0),
            commission=data.get("commission", 0.0),
        )

    def __str__(self) -> str:
        return f"{format_date(self.date)} | {str(self.mcc_code)} | {format_amount(self.amount, str(self.currency_code))}"
