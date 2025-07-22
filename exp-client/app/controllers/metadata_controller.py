class MetaDataController:
    """
    Provides cached access to currency and category metadata.
    Args:
        currency_service: Service for currency data operations
        category_service: Service for category data operations
    """
    def __init__(self, currency_service, category_service):
        self.currency_service = currency_service
        self.category_service = category_service
        self._currencies_cache = None
        self._categories_cache = None

    def get_currencies(self, force_refresh: bool = False) -> list:
        if self._currencies_cache is None or force_refresh:
            currencies, _ = self.currency_service.get_currencies()
            self._currencies_cache = currencies
        return self._currencies_cache

    def get_currency_name_by_code(self, code: int) -> str:
        return next((c.name for c in self.get_currencies() if c.currency_code == code), str(code))

    def get_categories(self, force_refresh: bool = False) -> list:
        if self._categories_cache is None or force_refresh:
            categories, _ = self.category_service.get_categories()
            self._categories_cache = categories
        return self._categories_cache

    def get_category_name_by_mcc(self, mcc: int) -> str:
        return next((c.name for c in self.get_categories() if c.mcc_code == mcc), str(mcc))
