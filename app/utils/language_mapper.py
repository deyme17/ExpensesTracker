from app.text.uk.transaction import TRANSACTION_TYPES, PAYMENT_METHODS, FIELDS
from app.text.uk.analytics import CHART_TYPES
from app.text.uk.categories import CATEGORIES
from app.text.uk.messages import MESSAGES
from app.text.uk.messages.months import LONG_MONTHS, SHORT_MONTHS

class LanguageMapper:

    @staticmethod
    def transaction_type(key: str) -> str:
        return TRANSACTION_TYPES.get(key, key)

    @staticmethod
    def payment_method(key: str) -> str:
        return PAYMENT_METHODS.get(key, key)

    @staticmethod
    def field_name(key: str) -> str:
        return FIELDS.get(key, key)

    @staticmethod
    def chart_type(key: str) -> str:
        return CHART_TYPES.get(key, key)

    @staticmethod
    def category(key: str) -> str:
        return CATEGORIES.get(key, key)

    @staticmethod
    def message(key: str) -> str:
        return MESSAGES.get(key, key)

    @staticmethod
    def months(short: bool = False) -> list[str]:
        return SHORT_MONTHS if short else LONG_MONTHS
