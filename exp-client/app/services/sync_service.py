class SyncService:
    """
    Service for synchronizing financial data between local storage and external sources.
    Args:
        local_storage: Local storage handler with data repositories
        transaction_data: List of transactions to synchronize
        category_data: List of categories to synchronize  
        currency_data: List of currencies to synchronize
    """
    def __init__(self, local_storage, transaction_data, category_data, currency_data):
        self.local_storage = local_storage
        self.transactions = transaction_data
        self.categories = category_data
        self.currencies = currency_data

    def sync(self):
        """
        Performs full synchronization of all data types.
        Executes in following order:
            - Transactions sync
            - Categories sync  
            - Currencies sync
        """
        self._sync_transactions()
        self._sync_categories()
        self._sync_currencies()

    def _sync_transactions(self):
        """
        Synchronizes transactions data.
        Only saves transactions that don't already exist in local storage.
        """
        existing_ids = set(t.transaction_id for t in self.local_storage.transactions.get_transactions())
        new_transactions = [t for t in self.transactions if t.transaction_id not in existing_ids]
        if new_transactions:
            self.local_storage.transactions.save_transactions(new_transactions)

    def _sync_categories(self):
        """
        Synchronizes categories data.
        Only saves categories with new MCC codes not present locally.
        """
        existing = {c.mcc_code for c in self.local_storage.categories.get_categories()}
        new = [c for c in self.categories if c.mcc_code not in existing]
        if new:
            self.local_storage.categories.save_categories(new)

    def _sync_currencies(self):
        """
        Synchronizes currencies data.
        Only saves currencies with new currency codes not present locally.
        """
        existing = {c.currency_code for c in self.local_storage.currencies.get_currencies()}
        new = [c for c in self.currencies if c.currency_code not in existing]
        if new:
            self.local_storage.currencies.save_currencies(new)