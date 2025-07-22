from app.api import (
    api_get_transactions,
    api_add_transaction,
    api_update_transaction,
    api_delete_transaction,
    api_get_transaction_by_id
)
from app.models.transaction import Transaction
from app.utils.helpers import RemoteMode
from app.utils.error_codes import ErrorCodes
from app.utils.formatters import format_date


class TransactionService(RemoteMode):
    """
    Handles transaction operations including CRUD and caching.
    Args:
        user_id: ID of the current user
        local_storage: Storage handler for offline operations (must implement
                       `get_transactions()` and `save_transactions()`)
    """
    def __init__(self, user_id: str|None, local_storage):
        self.user_id = user_id
        self.local_storage = local_storage
        self._cached = None

    def get_transactions(self, force_refresh: bool = False) -> tuple[list[Transaction], str | None]:
        """
        Retrieves transactions from cache, API, or local storage.
        Args:
            force_refresh: If True, bypasses cache
        Returns:
            Tuple: (list_of_transactions, error_message or None)
        """
        # use local storage if offline
        if self.offline_mode or not self.user_id:
            try:
                transactions = self.local_storage.transactions.get_transactions()
                return transactions, None
            except Exception:
                return [], ErrorCodes.OFFLINE_MODE

        # cache?
        if self._cached is not None and not force_refresh:
            return self._cached, None

        # api
        try:
            result = api_get_transactions(self.user_id)
            if result.get("success"):
                transactions = [Transaction.from_dict(t) for t in result["data"]]
                self._cached = transactions
                return transactions, None

            return [], result.get("error", ErrorCodes.UNKNOWN_ERROR)

        except Exception:
            try:
                transactions = self.local_storage.transactions.get_transactions()
                return transactions, ErrorCodes.API_FAILED_BUT_LOADED_LOCAL
            except Exception:
                return [], ErrorCodes.UNKNOWN_ERROR

    def get_transaction_by_id(self, transaction_id: str):
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

    def post_transaction(self, data: dict) -> dict:
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
            try:
                formatted = format_date(date_str, "%Y-%m-%d")
                data["date"] = formatted
            except ValueError:
                print(f"[TransactionService] Invalid date format: {date_str}")
                return {"success": False, "error": ErrorCodes.INVALID_DATE_FORMAT}

        result = api_add_transaction(data)
        if result.get("success"):
            self._invalidate_cache()
        return result

    def patch_transaction(self, transaction_id: str, data: dict) -> dict:
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

    def delete_transaction(self, transaction_id: str) -> dict:
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
            if self.local_storage:
                self.local_storage.transactions.save_transactions(self._cached)
        return result

    def _invalidate_cache(self):
        """Clears the internal transactions cache."""
        self._cached = None
