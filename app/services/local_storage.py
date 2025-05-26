import json
import os
from datetime import datetime
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.account import Account
from app.models.currency import Currency


class LocalStorageService:    
    def __init__(self, storage_dir=None):
        if storage_dir is None:
            home_dir = os.path.expanduser("~")
            self.storage_dir = os.path.join(home_dir, ".expenses_tracker")
        else:
            self.storage_dir = storage_dir

        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

        self.user_file = os.path.join(self.storage_dir, "user.json")
        self.transactions_file = os.path.join(self.storage_dir, "transactions.json")
        self.categories_file = os.path.join(self.storage_dir, "categories.json")
        self.accounts_file = os.path.join(self.storage_dir, "accounts.json")
        self.currencies_file = os.path.join(self.storage_dir, "currencies.json")
        self.active_account_file = os.path.join(self.storage_dir, "active_account.txt")

    # user
    def save_user(self, user):
        if not user:
            return
        with open(self.user_file, "w", encoding="utf-8") as f:
            json.dump(user.to_dict(), f, ensure_ascii=False, indent=2)

    def get_user(self):
        if not os.path.exists(self.user_file):
            return None
        try:
            with open(self.user_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return User.from_dict(data)
        except Exception:
            return None

    def clear_user(self):
        if os.path.exists(self.user_file):
            os.remove(self.user_file)

    # transactions
    def save_transactions(self, transactions):
        if not transactions:
            return
        transaction_dicts = [t.to_dict() for t in transactions]
        with open(self.transactions_file, "w", encoding="utf-8") as f:
            json.dump(transaction_dicts, f, ensure_ascii=False, indent=2)

    def get_transactions(self, force_refresh=False):
        if not os.path.exists(self.transactions_file):
            return []
        try:
            with open(self.transactions_file, "r", encoding="utf-8") as f:
                transaction_dicts = json.load(f)
            return [Transaction.from_dict(td) for td in transaction_dicts]
        except Exception:
            return []

    def add_transaction(self, transaction):
        if not transaction:
            return
        transactions = self.get_transactions()
        transactions.append(transaction)
        self.save_transactions(transactions)

    def update_transaction(self, transaction):
        if not transaction:
            return
        transactions = self.get_transactions()
        for i, t in enumerate(transactions):
            if t.transaction_id == transaction.transaction_id:
                transactions[i] = transaction
                break
        self.save_transactions(transactions)

    def delete_transaction(self, transaction_id):
        transactions = self.get_transactions()
        transactions = [t for t in transactions if t.transaction_id != transaction_id]
        self.save_transactions(transactions)

    def get_transaction(self, transaction_id):
        for t in self.get_transactions():
            if t.transaction_id == transaction_id:
                return t
        return None

    # accounts
    def save_accounts(self, accounts):
        if not accounts:
            return
        data = [a.to_dict() for a in accounts]
        with open(self.accounts_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_accounts(self):
        if not os.path.exists(self.accounts_file):
            return []
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Account.from_dict(a) for a in data]
        except Exception:
            return []

    def set_active_account(self, account_id):
        with open(self.active_account_file, "w") as f:
            f.write(account_id)

    def get_active_account_id(self):
        try:
            with open(self.active_account_file, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    # categories
    def save_categories(self, categories):
        if not categories:
            return
        data = [c.to_dict() for c in categories]
        with open(self.categories_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_categories(self):
        if not os.path.exists(self.categories_file):
            return []
        try:
            with open(self.categories_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Category.from_dict(c) for c in data]
        except Exception:
            return []

    # currencies
    def save_currencies(self, currencies):
        if not currencies:
            return
        data = [c.to_dict() for c in currencies]
        with open(self.currencies_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_currencies(self):
        if not os.path.exists(self.currencies_file):
            return []
        try:
            with open(self.currencies_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Currency.from_dict(c) for c in data]
        except Exception:
            return []

    def close(self):
        pass