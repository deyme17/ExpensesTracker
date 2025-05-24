from app.services.transactions.transaction_service import BaseTransactionService
from app.services.api_service import (
    api_get_transactions,
    api_add_transaction,
    api_delete_transaction,
    api_update_transaction
)
from app.models.transaction import Transaction
from app.utils.language_mapper import LanguageMapper as LM

class RemoteTransactionService(BaseTransactionService):
    def __init__(self, user_id):
        self.user_id = user_id

    def add_transaction(self, **kwargs):
        try:
            data = kwargs.copy()
            data["user_id"] = self.user_id
            response = api_add_transaction(data)
            if response.get("success"):
                return True, LM.message("add_success")
            return False, response.get("error", LM.message("server_error"))
        except Exception as e:
            return False, LM.message("server_error") + f" ({e})"

    def update_transaction(self, transaction_id, **kwargs):
        try:
            response = api_update_transaction(transaction_id, kwargs)
            if response.get("success"):
                return True, LM.message("update_success")
            return False, response.get("error", LM.message("server_error"))
        except Exception as e:
            return False, LM.message("server_error") + f" ({e})"

    def delete_transaction(self, transaction_id):
        try:
            response = api_delete_transaction(transaction_id)
            if response.get("success"):
                return True, LM.message("delete_success")
            return False, response.get("error", LM.message("unable_delete_transaction"))
        except Exception as e:
            return False, LM.message("unable_delete_transaction") + f" ({e})"

    def get_transaction_by_id(self, transaction_id):
        return None

    def get_transactions(self, force_refresh=False):
        try:
            raw_list = api_get_transactions(self.user_id)
            return [Transaction.from_dict(t) for t in raw_list]
        except Exception:
            return []