class TransactionProcessor:
    """
    Provides transaction filtering and sorting operations.
    Args:
        category_service: Provides MCC code lookups and category management.
    """
    def __init__(self, category_service):
        self.category_service = category_service

    def filter(self, transactions, min_amount=0, max_amount=float('inf'),
            start_date=None, end_date=None, type=None,
            payment_method=None, category=None, account_id=None):
        """Filters transactions based on multiple criteria.
        Args:
            transactions: List of Transaction objects to filter
            min_amount: Minimum absolute amount (default: 0)
            max_amount: Maximum absolute amount (default: no limit)
            start_date: Minimum date (inclusive, default: no limit)
            end_date: Maximum date (inclusive, default: no limit) 
            type: Transaction type to match (default: any)
            payment_method: Payment method to match (default: any)
            category: Category name to match (default: any)
            account_id: Account ID to match (default: any)
        Returns:
            List[Transaction]: Filtered transactions
        """
        def predicate(tx):
            tx_category_name = self.category_service.get_category_name_by_mcc(tx.mcc_code)
            return all([
                min_amount <= abs(tx.amount) <= max_amount,
                (start_date is None or tx.date >= start_date),
                (end_date is None or tx.date <= end_date),
                (type is None or tx.type == type),
                (payment_method is None or tx.payment_method == payment_method),
                (category is None or tx_category_name == category),
                (account_id is None or tx.account_id == account_id)
            ])

        return [tx for tx in transactions if predicate(tx)]

    def sort(self, transactions, field="date", ascending=True):
        """Sorts transactions by specified field.
        Args:
            transactions: List of Transaction objects to sort
            field: Field to sort by ('date', 'amount', 'cashback', 'commission')
                   Defaults to 'date'
            ascending: Sort direction (default: True)
        Returns:
            List[Transaction]: Sorted transactions
        Note:
            For invalid sort fields, returns original list unsorted
        """
        key_funcs = {
            "date": lambda t: t.date,
            "amount": lambda t: abs(t.amount),
            "cashback": lambda t: float(t.cashback or 0),
            "commission": lambda t: float(t.commission or 0)
        }

        key_func = key_funcs.get(field.lower())
        if not key_func:
            return transactions

        return sorted(transactions, key=key_func, reverse=not ascending)