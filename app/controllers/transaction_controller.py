from app.services.transaction_processor import TransactionProcessor

class TransactionController:
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

    def filter_transactions(self, *, is_income=None, start_date=None, end_date=None, min_amount=None, max_amount=None, payment_method=None):
        transactions = self.get_transactions()
        return TransactionProcessor.filter(
            transactions,
            is_income=is_income,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount,
            payment_method=payment_method
        )

    def sort_transactions(self, transactions, field='date', ascending=True):
        return TransactionProcessor.sort(transactions, field, ascending)
