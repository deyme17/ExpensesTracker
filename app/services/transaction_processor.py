from datetime import datetime

class TransactionProcessor:
    @staticmethod
    def filter(transactions, min_amount=0, max_amount=float('inf'),
               start_date=None, end_date=None, type=None,
               payment_method=None, category=None):
        result = []
        for tx in transactions:
            if tx.amount < min_amount or tx.amount > max_amount:
                continue
            if start_date and tx.date < start_date:
                continue
            if end_date and tx.date > end_date:
                continue
            if type and type != "усі" and tx.type != type:
                continue
            if payment_method and tx.payment_method != payment_method:
                continue
            if category and tx.category != category:
                continue
            result.append(tx)
        return result

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
