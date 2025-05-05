from datetime import datetime

class TransactionProcessor:
    @staticmethod
    def filter(transactions, *, is_income=None, start_date=None, end_date=None, min_amount=None, max_amount=None, payment_method=None):
        filtered = transactions

        if is_income is not None:
            filtered = [t for t in filtered if t.is_income == is_income]

        if start_date:
            filtered = [t for t in filtered if t.date >= start_date]
        if end_date:
            filtered = [t for t in filtered if t.date <= end_date]

        if min_amount is not None:
            filtered = [t for t in filtered if abs(t.amount) >= min_amount]
        if max_amount is not None:
            filtered = [t for t in filtered if abs(t.amount) <= max_amount]

        if payment_method:
            filtered = [t for t in filtered if t.payment_method == payment_method]

        return filtered

    @staticmethod
    def sort(transactions, field='date', ascending=True):
        key_funcs = {
            'date': lambda t: t.date,
            'amount': lambda t: abs(t.amount),
            'cashback': lambda t: float(t.cashback or 0),
            'commission': lambda t: float(t.commission or 0)
        }

        key_func = key_funcs.get(field.lower())
        if not key_func:
            return transactions

        return sorted(transactions, key=key_func, reverse=not ascending)
