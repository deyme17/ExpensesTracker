from datetime import datetime

class TransactionProcessor:
    @staticmethod
    def filter(transactions, min_amount=0, max_amount=float('inf'),
            start_date=None, end_date=None, type=None,
            payment_method=None, category=None, account_id=None):
        def predicate(tx):
            return all([
                min_amount <= abs(tx.amount) <= max_amount,
                (start_date is None or tx.date >= start_date),
                (end_date is None or tx.date <= end_date),
                (type is None or tx.type == type),
                (payment_method is None or tx.payment_method == payment_method),
                (category is None or tx.category == category),
                (account_id is None or tx.account_id == account_id)
            ])

        return [tx for tx in transactions if predicate(tx)]

    @staticmethod
    def sort(transactions, field="date", ascending=True):
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
