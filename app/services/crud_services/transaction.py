from app.services.api import (
    api_get_transactions,
    api_add_transaction,
    api_update_transaction,
    api_delete_transaction,
    api_get_transaction_by_id
)
from app.models.transaction import Transaction
from app.utils.connection_manager import ConnectionManager
from app.utils.error_codes import ErrorCodes

class TransactionService:
    def __init__(self, user_id, storage_service):
        self.user_id = user_id
        self.storage = storage_service
        self.offline_mode = not ConnectionManager.is_online()
        self._cached = None

    def get_transactions(self, force_refresh=False):
        if self.offline_mode:
            print("[TransactionService] OFFLINE mode: loading from local storage")
            return self.storage.get_transactions()

        if self._cached is not None and not force_refresh:
            return self._cached

        result = api_get_transactions(self.user_id)
        if result.get("success"):
            transactions = [Transaction.from_dict(t) for t in result["data"]]
            self._cached = transactions
            if self.storage:
                self.storage.save_transactions(transactions)
            return transactions
        else:
            print("[TransactionService] API error:", result.get("error"))
            return self.storage.get_transactions()

    def get_transaction_by_id(self, transaction_id):
        result = api_get_transaction_by_id(transaction_id)
        if result.get("success"):
            return Transaction.from_dict(result["data"])
        print("[TransactionService] get by id error:", result.get("error"))
        return None

    def post_transaction(self, data):
        data["user_id"] = self.user_id
        result = api_add_transaction(data)
        if result.get("success"):
            self._invalidate_cache()
        return result

    def patch_transaction(self, transaction_id, data):
        result = api_update_transaction(transaction_id, data)
        if result.get("success"):
            self._invalidate_cache()
        return result

    def delete_transaction(self, transaction_id):
        result = api_delete_transaction(transaction_id)
        if result.get("success"):
            if self._cached:
                self._cached = [t for t in self._cached if t.transaction_id != transaction_id]
            if self.storage:
                self.storage.save_transactions(self._cached)
        return result

    def _invalidate_cache(self):
        self._cached = None
