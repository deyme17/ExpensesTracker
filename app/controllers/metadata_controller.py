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

    def get_currency_list(self, force_refresh=False):
        if self._currencies_cache is None or force_refresh:
            self._currencies_cache = self.currency_service.get_currency_list()
        return self._currencies_cache

    def get_currency_name_by_code(self, code):
        return next((c.name for c in self.get_currency_list() if c.currency_code == code), str(code))

    def get_category_list(self, force_refresh=False):
        if self._categories_cache is None or force_refresh:
            self._categories_cache = self.category_service.get_categories()
        return self._categories_cache

    def get_category_name_by_mcc(self, mcc):
        return next((c.name for c in self.get_category_list() if c.mcc_code == mcc), str(mcc))
