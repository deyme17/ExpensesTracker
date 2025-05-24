from datetime import datetime
from app.utils.formatters import format_amount, format_date
from kivy.app import App

class Transaction:
    def __init__(self, transaction_id, user_id, amount, date, account_id, category,
                 description="", payment_method="card", currency="UAH", type='expense',
                 cashback=0.0, commission=0.0, is_synced=True):

        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = float(amount)

        if isinstance(date, str):
            try:
                self.date = datetime.strptime(date, '%d.%m.%Y')
            except ValueError:
                try:
                    self.date = datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    self.date = datetime.now()
        else:
            self.date = date

        self.account_id = account_id
        self.type = type
        self.category = category
        self.description = description
        self.payment_method = payment_method
        self.currency = currency
        self.cashback = float(cashback)
        self.commission = float(commission)
        self.is_synced = is_synced

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "account_id": self.account_id,
            "type": self.type,
            "category": self.category,
            "description": self.description,
            "payment_method": self.payment_method,
            "currency": self.currency,
            "cashback": self.cashback,
            "commission": self.commission,
            "is_synced": self.is_synced
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None

        date = data.get("date")
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                date = datetime.now()

        return cls(
            transaction_id=data.get("transaction_id"),
            user_id=data.get("user_id"),
            amount=data.get("amount", 0.0),
            date=date,
            account_id=data.get("account_id"),
            category=data.get("category", ""),
            description=data.get("description", ""),
            payment_method=data.get("payment_method", "card"),
            currency=data.get("currency", "UAH"),
            cashback=data.get("cashback", 0.0),
            commission=data.get("commission", 0.0),
            is_synced=data.get("is_synced", True),
            type=data.get("type", "expense")
        )

    @classmethod
    def from_monobank(cls, data, user_id, account_id):
        app = App.get_running_app()
        static_data = app.static_data_service

        amount = data.get("amount", 0) / 100.0
        category = static_data.get_category_name_by_mcc(data.get("mcc", 0))
        currency = static_data.get_currency_code_by_number(data.get("currencyCode", 980))

        return cls(
            transaction_id=data.get("id"),
            user_id=user_id,
            amount=amount,
            date=datetime.fromtimestamp(data.get("time", datetime.now().timestamp())),
            account_id=account_id,
            category=category,
            type="income" if amount > 0 else "expense",
            description=data.get("description", ""),
            payment_method="card",
            currency=currency,
            cashback=data.get("cashbackAmount", 0) / 100.0,
            commission=data.get("commissionRate", 0) / 100.0,
            is_synced=True
        )

    def __str__(self):
        return f"{format_date(self.date)} | {self.category} | {format_amount(self.amount, self.currency)}"