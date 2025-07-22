class Account:
    def __init__(self, account_id: str, user_id: str, type: str, currency_code: int|str, balance: float, masked_pan: str = None):
        self.account_id = account_id
        self.user_id = user_id
        self.type = type
        self.currency_code = int(currency_code)
        self.balance = balance
        self.masked_pan = masked_pan

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "type": self.type,
            "currency_code": self.currency_code,
            "balance": self.balance,
            "masked_pan": self.masked_pan
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Account':
        return cls(
            account_id=data.get("account_id"),
            user_id=data.get("user_id"),
            type=data.get("type"),
            currency_code=data.get("currency_code"),
            balance=data.get("balance"),
            masked_pan=data.get("masked_pan")
        )