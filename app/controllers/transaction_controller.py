from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
from datetime import datetime


class TransactionController:
    """
    Handles business logic for transaction operations including CRUD, filtering, and sorting.
    Args:
        transaction_service: Service layer for direct transaction database operations.
        transaction_processor: Handles complex transaction processing like filtering rules.
        category_service: Provides MCC code lookups and category management.
        currency_service: Manages currency conversions and code lookups.
    """
    def __init__(self, transaction_service, transaction_processor, category_service, currency_service):
        self.transaction_processor = transaction_processor
        self.transaction_service = transaction_service
        self.category_service = category_service
        self.currency_service = currency_service

    def add_transaction(self, **kwargs) -> dict:
        return self.transaction_service.post_transaction(**kwargs)

    def update_transaction(self, transaction_id: str, category: str, amount: str|float, date: datetime,
                           description: str, payment_method: str, currency: str, cashback: str|float,
                           commission: str|float, account_id: str) -> dict:
        try:
            mcc_code = int(self.category_service.get_mcc_by_name(category))
            currency_code = int(self.currency_service.get_currency_code_by_name(currency))

            data = {
                "mcc_code": mcc_code,
                "amount": float(amount),
                "date": date,
                "description": description,
                "payment_method": payment_method,
                "currency_code": currency_code,
                "cashback": float(cashback or 0),
                "commission": float(commission or 0),
                "account_id": account_id,
            }

            if transaction_id:
                result = self.transaction_service.patch_transaction(transaction_id, data)
            else:
                result = self.transaction_service.post_transaction(data)

            if result.get("success"):
                return True, ""
            else:
                code = result.get("error", ErrorCodes.UNKNOWN_ERROR)
                return False, LM.server_error(code)

        except Exception:
            return False, LM.server_error(ErrorCodes.UNKNOWN_ERROR)

    def delete_transaction(self, transaction_id: str) -> tuple[bool, str]:
        result = self.transaction_service.delete_transaction(transaction_id)
        if result.get("success"):
            return True, "transaction_deleted"
        return False, LM.server_error(result.get("error", ErrorCodes.UNKNOWN_ERROR))

    def get_transaction_by_id(self, transaction_id: str):
        return self.transaction_service.get_transaction_by_id(transaction_id)

    def get_transactions(self, force_refresh: bool = False) -> list:
        return self.transaction_service.get_transactions(force_refresh=force_refresh)

    def filter_transactions(self, *, type: str = None, start_date: datetime = None, end_date: datetime = None,
                            min_amount: str|int|float = 0, max_amount: str|int|float = 1e9, payment_method: str = None,
                            category: str = None, account_id: str = None) -> list:
        transactions = self.get_transactions()
        return self.transaction_processor.filter(
            transactions,
            type=type,
            start_date=start_date,
            end_date=end_date,
            min_amount=float(min_amount),
            max_amount=float(max_amount),
            payment_method=payment_method,
            category=category,
            account_id=account_id
        )

    def sort_transactions(self, transactions: list, field: str = 'date', ascending: bool = True) -> list:
        """Sorts transactions by specified field and direction."""
        return self.transaction_processor.sort(transactions, field, ascending)