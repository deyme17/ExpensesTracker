from app.models.currency import Currency
from app.api import api_get_currencies
from app.utils.constants import DEFAULT_CURRENCY_CODE
from app.utils.error_codes import ErrorCodes


class CurrencyService:
    """
    Handles currency data operations including code/name conversions and caching.
    Args:
        local_storage: Optional storage service for local caching (must implement 
                       `save_currencies()` and `get_currencies()`)
    """
    def __init__(self, local_storage=None):
        self.local_storage = local_storage
        # cache
        self._code_to_currency = {}
        self._name_to_currency_code = {}

    def get_currencies(self) -> tuple[list, str]:
        """
        Retrieves currencies from cache, API, or local storage (in priority order).
        Returns:
            Tuple: (list_of_currencies, error_message)
        """
        if self._code_to_currency:
            return [Currency(currency_code=k, name=v) for k, v in self._code_to_currency.items()], None

        try:
            result = api_get_currencies()
            if result.get("success"):
                currencies = [Currency.from_dict(c) for c in result["data"]]

                if self.local_storage:
                    self.local_storage.currencies.save_currencies(currencies)

                self._update_currency_cache(currencies)
                return currencies, None
            
            return [], result.get("error", ErrorCodes.UNKNOWN_ERROR)
        except Exception:
            pass

        if self.local_storage:
            currencies = self.local_storage.currencies.get_currencies()
            self._update_currency_cache(currencies)
            return currencies, ErrorCodes.OFFLINE_MODE

        return [], ErrorCodes.UNKNOWN_ERROR

    def _update_currency_cache(self, currencies: list):
        """
        Updates internal currency code/name mappings.
        Args:
            currencies: List of Currency objects
        """
        self._code_to_currency = {str(c.currency_code): c.name for c in currencies}
        self._name_to_currency_code = {v: str(k) for k, v in self._code_to_currency.items()}

    def get_currency_name_by_code(self, currency_code: int|str) -> str:
        """
        Gets currency name for given currency code.
        Args:
            currency_code: String or numeric currency code
        Returns:
            str: Currency name if found, currency_code as string otherwise
        """
        if not self._code_to_currency:
            currencies, _ = self.get_currencies()
            if currencies:
                self._update_currency_cache(currencies)
        return self._code_to_currency.get(str(currency_code), str(currency_code))

    def get_currency_code_by_name(self, name: str) -> str:
        """
        Gets currency code for given currency name.
        Args:
            name: Currency name string
        Returns:
            str: Currency code or DEFAULT_CURRENCY_CODE if not found
        """
        if not self._name_to_currency_code:
            currencies, _ = self.get_currencies()
            if currencies:
                self._update_currency_cache(currencies)
        return str(self._name_to_currency_code.get(name, DEFAULT_CURRENCY_CODE))