from sqlalchemy.orm import Session
from app.database.orm_models import Category
from app.services.bank_services.bank_service import BankService


class BankSyncService:
    """
    Synchronizes user data from a bank service: accounts, transactions, categories.
    """
    def __init__(self, account_service, transaction_service, category_service):
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.category_service = category_service

    def sync_user_data(self, bank: BankService, user_id: str, db: Session) -> None:
        """
        Syncs accounts and transactions for the given user from bank data.
        """
        try:
            client_info = bank.get_client_info()
            accounts = self._add_accounts(client_info, user_id, db)
            transactions = self._get_transactions(bank, accounts, user_id)
            self._add_missing_categories(transactions, db)
            self._add_transactions(transactions, db)
            db.commit()
        except Exception:
            db.rollback()
            raise

    def _add_accounts(self, client_info: dict, user_id: str, db: Session):
        """
        Creates accounts from bank client info and returns them.
        """
        accounts_data = client_info.get("accounts", [])
        if not accounts_data:
            raise Exception("no_accounts_found")
        return self.account_service.repo.bulk_create(accounts_data, user_id, db)

    def _get_transactions(self, bank: BankService, accounts: list, user_id: str):
        """
        Retrieves and maps transactions for all accounts.
        """
        all_transactions = []
        for acc in accounts:
            txs = bank.get_transactions(acc.account_id, days=31)
            mapped = self.transaction_service.map_transactions(txs, user_id, acc.account_id)
            all_transactions.extend(mapped)
        return all_transactions

    def _add_missing_categories(self, transactions: list, db: Session):
        """
        Adds MCC categories that are missing in the database.
        """
        existing_mcc = self.category_service.get_existing_mcc_codes()
        missing_mcc = {t.mcc_code for t in transactions if t.mcc_code not in existing_mcc}
        for code in missing_mcc:
            db.add(Category(mcc_code=code, name="other"))

    def _add_transactions(self, transactions: list, db: Session):
        """
        Adds mapped transactions to the database.
        """
        for tx in transactions:
            db.add(tx)
