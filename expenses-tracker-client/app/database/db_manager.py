from app.database.repositories import (AccountRepository, CategoryRepository, CurrencyRepository, 
                                       TransactionRepository, UserRepository, SettingsRepository)
from app.database.orm_models.base_orm import SessionLocal


class LocalDBManager:
    """Centralized database access manager for local SQLite storage.
    Provides repositories for all core entities:
        - Accounts
        - Categories  
        - Currencies
        - Transactions
        - Users
        - Settings
    """
    def __init__(self):
        self.session = SessionLocal()
        self.accounts = AccountRepository(self.session)
        self.categories = CategoryRepository(self.session)
        self.currencies = CurrencyRepository(self.session)
        self.transactions = TransactionRepository(self.session)
        self.user = UserRepository(self.session)
        self.settings = SettingsRepository(self.session)

    def close(self):
        """Close database session"""
        try:
            self.session.close()
        except Exception as e:
            print(f"[ERROR] Failed to close database session: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()