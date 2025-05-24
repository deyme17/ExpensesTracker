from app.services.transactions.transaction_service import BaseTransactionService

class LocalTransactionService(BaseTransactionService):
    def __init__(self, storage_service):
        self.storage_service = storage_service

    def add_transaction(self, **kwargs):
        return self.storage_service.add_transaction(**kwargs)

    def update_transaction(self, transaction_id, **kwargs):
        return self.storage_service.update_transaction(transaction_id, **kwargs)

    def delete_transaction(self, transaction_id):
        return self.storage_service.delete_transaction(transaction_id)

    def get_transaction_by_id(self, transaction_id):
        return self.storage_service.get_transaction_by_id(transaction_id)

    def get_transactions(self, force_refresh=False):
        return self.storage_service.get_transactions(force_refresh=force_refresh)