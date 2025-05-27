class Account:
    def __init__(self, account_id, user_id, type, currency_code, balance, masked_pan=None):
        self.account_id = account_id
        self.user_id = user_id
        self.type = type
        self.currency_code = currency_code
        self.balance = balance
        self.masked_pan = masked_pan

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "type": self.type,
            "currency_code": self.currency_code,
            "balance": self.balance,
            "masked_pan": self.masked_pan
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            account_id=data.get("account_id"),
            user_id=data.get("user_id"),
            type=data.get("type"),
            currency_code=data.get("currency_code"),
            balance=data.get("balance"),
            masked_pan=data.get("masked_pan")
        )

    @classmethod
    def from_monobank_dict(cls, data, user_id):
        return cls(
            account_id=data.get("id"),
            user_id=user_id,
            type=data.get("type"),
            currency_code=data.get("currencyCode"),
            balance=data.get("balance", 0) / 100.0,
            masked_pan=data.get("maskedPan", [None])[0]
        )
