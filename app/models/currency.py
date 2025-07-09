class Currency:
    def __init__(self, currency_code: int|str, name: str):
        self.currency_code = int(currency_code)
        self.name = name

    def to_dict(self) -> dict:
        return {
            "currency_code": self.currency_code,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Currency':
        return cls(
            currency_code=data.get("currency_code"),
            name=data.get("name")
        )