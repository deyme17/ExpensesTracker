from app.api import (
    api_get_transactions,
    api_add_transaction,
    api_update_transaction,
    api_delete_transaction,
    api_get_transaction_by_id
)
from app.models.transaction import Transaction
from app.utils.helpers import is_online
from app.utils.error_codes import ErrorCodes
from app.utils.formatters import format_date


class TransactionService:
    """
    Handles transaction operations including CRUD and caching.
    Args:
        user_id: ID of the current user
        storage_service: Storage handler for offline operations (must implement
                       `get_transactions()` and `save_transactions()`)
    """
    def __init__(self, user_id, storage_service):
        self.user_id = user_id
        self.storage = storage_service
        self.offline_mode = not is_online()
        self._cached = None

    def get_transactions(self, force_refresh=False):
        """
        Retrieves transactions from cache, API, or local storage.
        Args:
            force_refresh: If True, bypasses cache
        Returns:
            List[Transaction]: List of transaction objects
        """
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
        """
        Gets single transaction by ID.
        Args:
            transaction_id: ID of transaction to retrieve
        Returns:
            Transaction or None if not found
        """
        result = api_get_transaction_by_id(transaction_id)
        if result.get("success"):
            return Transaction.from_dict(result["data"])
        print("[TransactionService] get by id error:", result.get("error"))
        return None

    def post_transaction(self, data):
        """
        Creates a new transaction.
        Args:
            data: Transaction data dict
        Returns:
            Dict: API response with success/error status
        """
        data["user_id"] = self.user_id

        date_str = data.get("date")
        if date_str:
            formatted = format_date(date_str, "%Y-%m-%d")
            if formatted == date_str:
                print(f"[TransactionService] Invalid date format: {date_str}")
                return {"success": False, "error": ErrorCodes.INVALID_DATE_FORMAT}
            data["date"] = formatted

        result = api_add_transaction(data)
        if result.get("success"):
            self._invalidate_cache()
        return result

    def patch_transaction(self, transaction_id, data):
        """
        Updates an existing transaction.
        Args:
            transaction_id: ID of transaction to update
            data: Partial transaction data
        Returns:
            Dict: API response with success/error status
        """
        date_str = data.get("date")
        if date_str:
            formatted = format_date(date_str, "%Y-%m-%d")
            if formatted == date_str: 
                print(f"[TransactionService] Invalid date format: {date_str}")
                return {"success": False, "error": ErrorCodes.INVALID_DATE_FORMAT}
            data["date"] = formatted

        result = api_update_transaction(transaction_id, data)
        if result.get("success"):
            self._invalidate_cache()
        return result

    def delete_transaction(self, transaction_id):
        """
        Deletes a transaction.
        Args:
            transaction_id: ID of transaction to delete
        Returns:
            Dict: API response with success/error status
        """
        result = api_delete_transaction(transaction_id)
        if result.get("success"):
            if self._cached:
                self._cached = [t for t in self._cached if t.transaction_id != transaction_id]
            if self.storage:
                self.storage.save_transactions(self._cached)
        return result

    def _invalidate_cache(self):
        """Clears the internal transactions cache."""
        self._cached = None
