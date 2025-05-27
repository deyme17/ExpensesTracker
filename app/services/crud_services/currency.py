import requests
from app.models.category import Category
from app.models.currency import Currency
from app.services.api import api_get_currencies, get_auth_headers
from app.utils.constants import DEFAULT_CURRENCY_CODE
from app.utils.error_codes import ErrorCodes

class CurrencyService:
    def __init__(self, storage_service=None):
        self.storage_service = storage_service
        self._code_to_currency = {}
        self._name_to_currency_code = {}

    def get_currencies(self):
        if self._code_to_currency:
            return [Currency(currency_code=k, name=v) for k, v in self._code_to_currency.items()], None

        try:
            result = api_get_currencies()
            if result.get("success"):
                currencies = [Currency.from_dict(c) for c in result["data"]]
                if self.storage_service:
                    self.storage_service.save_currencies(currencies)
                self._update_currency_cache(currencies)
                return currencies, None
            return [], result.get("error", ErrorCodes.UNKNOWN_ERROR)
        except Exception:
            pass

        if self.storage_service:
            currencies = self.storage_service.get_currencies()
            self._update_currency_cache(currencies)
            return currencies, ErrorCodes.OFFLINE_MODE

        return [], ErrorCodes.UNKNOWN_ERROR

    def _update_currency_cache(self, currencies):
        self._code_to_currency = {str(c.currency_code): c.name for c in currencies}
        self._name_to_currency_code = {v: str(k) for k, v in self._code_to_currency.items()}

    def get_currency_name_by_code(self, currency_code):
        if not self._code_to_currency:
            currencies, _ = self.get_currencies()
            if currencies:
                self._update_currency_cache(currencies)
        return self._code_to_currency.get(str(currency_code), str(currency_code))

    def get_currency_code_by_name(self, name):
        if not self._name_to_currency_code:
            currencies, _ = self.get_currencies()
            if currencies:
                self._update_currency_cache(currencies)
        return self._name_to_currency_code.get(name, DEFAULT_CURRENCY_CODE)