import requests
from app.models.category import Category
from app.models.currency import Currency
from app.services.api_service import api_get_categories, api_get_currencies, get_auth_headers
from app.utils.constants import DEFAULT_MCC, DEFAULT_CURRENCY_CODE


class StaticDataService:
    def __init__(self, storage_service=None):
        self.storage_service = storage_service
        self._mcc_to_name = {}
        self._name_to_mcc = {}
        self._code_to_currency = {}
        self._name_to_currency_code = {}

    def get_categories(self):
        if self._mcc_to_name:
            return [Category(mcc_code=k, name=v) for k, v in self._mcc_to_name.items()]

        try:
            result = api_get_categories()
            if result.get("success"):
                categories = [Category.from_dict(c) for c in result["data"]]
                if self.storage_service:
                    self.storage_service.save_categories(categories)
                self._update_category_cache(categories)
                return categories
        except Exception as e:
            print(f"[StaticDataService] category fetch error: {e}")

        if self.storage_service:
            categories = self.storage_service.get_categories()
            self._update_category_cache(categories)
            return categories

        return []

    def _update_category_cache(self, categories):
        self._mcc_to_name = {c.mcc_code: c.name for c in categories}
        self._name_to_mcc = {v: k for k, v in self._mcc_to_name.items()}

    def get_currencies(self):
        if self._code_to_currency:
            return [Currency(currency_code=k, name=v) for k, v in self._code_to_currency.items()]

        try:
            result = api_get_currencies()
            if result.get("success"):
                currencies = [Currency.from_dict(c) for c in result["data"]]
                if self.storage_service:
                    self.storage_service.save_currencies(currencies)
                self._update_currency_cache(currencies)
                return currencies
        except Exception as e:
            print(f"[StaticDataService] currency fetch error: {e}")

        if self.storage_service:
            currencies = self.storage_service.get_currencies()
            self._update_currency_cache(currencies)
            return currencies

        return []

    def _update_currency_cache(self, currencies):
        self._code_to_currency = {str(c.currency_code): c.name for c in currencies}
        self._name_to_currency_code = {v: str(k) for k, v in self._code_to_currency.items()}

    def get_category_name_by_mcc(self, mcc_code):
        if not self._mcc_to_name:
            categories = self.get_categories()
            self._update_category_cache(categories)
        return self._mcc_to_name.get(int(mcc_code), "other")

    def get_currency_name_by_code(self, currency_code):
        if not self._code_to_currency:
            currencies = self.get_currencies()
            if currencies:
                self._update_currency_cache(currencies)
        return self._code_to_currency.get(str(currency_code), str(currency_code))

    def get_mcc_by_name(self, name):
        if not self._name_to_mcc:
            categories = self.get_categories()
            self._update_category_cache(categories)
        return self._name_to_mcc.get(name, DEFAULT_MCC)

    def get_currency_code_by_name(self, name):
        if not self._name_to_currency_code:
            currencies = self.get_currencies()
            if currencies:
                self._update_currency_cache(currencies)
        return self._name_to_currency_code.get(name, DEFAULT_CURRENCY_CODE)
