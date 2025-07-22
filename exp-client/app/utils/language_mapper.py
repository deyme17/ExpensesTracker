from app.text.ua_localization.transaction_vars import TRANSACTION_TYPES, PAYMENT_METHODS, FIELDS
from app.text.ua_localization.messages.analytics import CHART_TYPES, STATS_FIELDS
from app.text.ua_localization.categories import CATEGORIES_MAP
from app.text.ua_localization.messages import MESSAGES
from app.text.ua_localization.months import LONG_MONTHS_MAP, SHORT_MONTHS_MAP
from app.text.ua_localization.messages.errors_messages import ERRORS

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
    def stat_name(key: str) -> str:
        return STATS_FIELDS.get(key, key)

    @staticmethod
    def category(key: str) -> str:
        return CATEGORIES_MAP.get(key, key)

    @staticmethod
    def message(key: str) -> str:
        return MESSAGES.get(key, key)

    @staticmethod
    def month_name(month_name_en: str, short: bool = True) -> str:
        if short:
            return SHORT_MONTHS_MAP.get(month_name_en, month_name_en)
        else:
            return LONG_MONTHS_MAP.get(month_name_en, month_name_en)
        
    @staticmethod
    def server_error(key: str) -> str:
        return ERRORS.get(key, key)