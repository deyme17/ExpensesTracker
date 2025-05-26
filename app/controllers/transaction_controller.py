from app.services.crud_services.transaction import TransactionService
from app.services.transaction_processor import TransactionProcessor
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes

class TransactionController:
    def __init__(self, transaction_service, static_service):
        self.transaction_service = transaction_service
        self.static_service = static_service

    def add_transaction(self, **kwargs):
        return self.transaction_service.add_transaction(**kwargs)

    def update_transaction(self, transaction_id, category, amount, date,
                           description, payment_method, currency, cashback,
                           commission, account_id):
        try:
            mcc_code = int(self.static_service.get_mcc_by_name(category))
            currency_code = int(self.static_service.get_currency_code_by_name(currency))

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

    def delete_transaction(self, transaction_id):
        result = self.transaction_service.delete_transaction(transaction_id)
        if result.get("success"):
            return True, "transaction_deleted"
        return False, LM.server_error(result.get("error", ErrorCodes.UNKNOWN_ERROR))

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