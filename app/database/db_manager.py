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
        self.session.close()