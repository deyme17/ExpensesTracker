from app.services.transactions.transaction_processor import TransactionProcessor
from app.services.transactions.transaction_service import BaseTransactionService

class TransactionController:
    def __init__(self, transaction_service: BaseTransactionService):
        self.transaction_service = transaction_service

    def add_transaction(self, **kwargs):
        return self.transaction_service.add_transaction(**kwargs)

    def update_transaction(self, transaction_id, **kwargs):
        return self.transaction_service.update_transaction(transaction_id, **kwargs)

    def delete_transaction(self, transaction_id):
        return self.transaction_service.delete_transaction(transaction_id)

    def get_transaction_by_id(self, transaction_id):
        return self.transaction_service.get_transaction_by_id(transaction_id)

    def get_transactions(self, force_refresh=False):
        return self.transaction_service.get_transactions(force_refresh=force_refresh)

    def filter_transactions(self, *, type=None, start_date=None, end_date=None, 
                            min_amount=0, max_amount=1e9, payment_method=None,
                            category=None, account_id=None):
        transactions = self.get_transactions()
        return TransactionProcessor.filter(
            transactions,
            type=type,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount,
            payment_method=payment_method,
            category=category,
            account_id=account_id
        )

    def sort_transactions(self, transactions, field='date', ascending=True):
        return TransactionProcessor.sort(transactions, field, ascending)