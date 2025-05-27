from datetime import datetime
from kivy.app import App
from app.utils.formatters import format_amount, format_date
from app.utils.constants import CARD, EXPENSE, DEFAULT_CURRENCY_CODE, INCOME


class Transaction:
    def __init__(self, transaction_id, user_id, amount, date, account_id,
                 mcc_code, currency_code, description="", payment_method=CARD, type=EXPENSE,
                 cashback=0.0, commission=0.0, is_synced=True):

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
        self.is_synced = is_synced

    def _parse_date(self, date):
        if isinstance(date, datetime):
            return date
        if isinstance(date, str):
            for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return datetime.strptime(date, fmt)
                except ValueError:
                    continue
        return datetime.now()

    def to_dict(self):
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
            "is_synced": self.is_synced
        }

    @classmethod
    def from_dict(cls, data):
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
            is_synced=data.get("is_synced", True)
        )

    @classmethod
    def from_monobank(cls, data, user_id, account_id):
        app = App.get_running_app()
        currency_service = app.currency_service

        amount = data.get("amount", 0) / 100.0
        mcc_code = data.get("mcc", 0)
        currency_code = currency_service.get_currency_code_by_number(data.get("currencyCode", 980))

        return cls(
            transaction_id=data.get("id"),
            user_id=user_id,
            amount=amount,
            date=datetime.fromtimestamp(data.get("time", datetime.now().timestamp())),
            account_id=account_id,
            type=INCOME if amount > 0 else EXPENSE,
            mcc_code=mcc_code,
            currency_code=currency_code,
            description=data.get("description", ""),
            payment_method="card",
            cashback=data.get("cashbackAmount", 0) / 100.0,
            commission=data.get("commissionRate", 0) / 100.0,
            is_synced=True
        )

    def __str__(self):
        try:
            app = App.get_running_app()
            category_service = app.category_service
            currency_service = app.currency_service
            
            category = category_service.get_category_name_by_mcc(self.mcc_code)
            currency = currency_service.get_currency_name_by_code(self.currency_code)
        except Exception:
            category = str(self.mcc_code)
            currency = str(self.currency_code)
        return f"{format_date(self.date)} | {category} | {format_amount(self.amount, currency)}"
