class Currency:
    def __init__(self, currency_code):
        self.currency_code = currency_code

    def to_dict(self):
        return {
            "currency_code": self.currency_code
        }

    @classmethod
    def from_dict(cls, data):
        return cls(currency_code=data.get("currency_code"))