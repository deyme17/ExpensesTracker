class Currency:
    def __init__(self, currency_code, name=None):
        self.currency_code = currency_code
        self.name = name

    def to_dict(self):
        return {
            "currency_code": self.currency_code,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            currency_code=data.get("currency_code"),
            name=data.get("name")
        )