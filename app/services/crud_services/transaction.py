from app.models.transaction import Transaction
from app.services.api_service import (
    api_get_transactions, api_add_transaction,
    api_update_transaction, api_delete_transaction
)
from app.services.local_storage import LocalStorageService as LM
from app.utils.connection_manager import ConnectionManager
from app.utils.language_mapper import LanguageMapper as LM
import uuid


class TransactionService:
    def __init__(self, user_id, storage_service):
        self.user_id = user_id
        self.storage = storage_service
        self.offline_mode = not ConnectionManager.is_online()
        self._cached = None

    def get_transactions(self, force_refresh=False):
        if self.offline_mode:
            return self.storage.get_transactions()

        if not force_refresh and self._cached:
            return self._cached

        try:
            result = api_get_transactions(self.user_id)
            if result.get("success"):
                transactions = [Transaction.from_dict(t) for t in result["data"]]
                self._cached = transactions
                self.storage.save_transactions(transactions)
                return transactions
        except Exception as e:
            print(f"[TransactionService] fetch error: {e}")

        return self.storage.get_transactions()

    def get_transaction_by_id(self, transaction_id):
        for tx in self.get_transactions():
            if tx.transaction_id == transaction_id:
                return tx
        return None

    def add_transaction(self, **kwargs):
        tx_id = kwargs.get("transaction_id") or str(uuid.uuid4())
        tx_dict = dict(kwargs)
        tx_dict["transaction_id"] = tx_id
        tx_dict["user_id"] = self.user_id

        # Ensure required fields
        tx_dict.setdefault("mcc_code", 0)
        tx_dict.setdefault("currency_code", "980")

        if self.offline_mode:
            transaction = Transaction.from_dict(tx_dict)
            self.storage.add_transaction(transaction)
            return True, LM.message("transaction_added_offline")

        try:
            response = api_add_transaction(tx_dict)
            return response.get("success", False), response.get("message", "")
        except Exception as e:
            return False, str(e)

    def update_transaction(self, transaction_id, **kwargs):
        if self.offline_mode:
            return self.storage.update_transaction(transaction_id, **kwargs)
        try:
            response = api_update_transaction(transaction_id, kwargs)
            return response.get("success", False), response.get("message", "")
        except Exception as e:
            return False, str(e)

    def delete_transaction(self, transaction_id):
        if self.offline_mode:
            self.storage.delete_transaction(transaction_id)
            return True, LM.message("transaction_deleted_offline")
        try:
            response = api_delete_transaction(transaction_id)
            return response.get("success", False), response.get("message", "")
        except Exception as e:
            return False, str(e)
