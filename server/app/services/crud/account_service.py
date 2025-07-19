from app.database.repositories.account_repository import AccountRepository
from sqlalchemy.orm import Session


class AccountService:
    """
    Service layer for account operations.
    Args:
        repository: AccountRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def create(self, data: dict, db: Session = None):
        """
        Creates a new account.
        Args:
            data: Account data dictionary
            db: Optional database session
        Returns:
            Created account object
        """
        return self.repo.create(data, db)
    
    def bulk_create(self, accounts_data: list[dict], user_id: str, db: Session = None):
        """
        Bulk create accounts.
        Args:
            accounts_data: list of account dicts from bank service
            user_id: user id to link accounts to
            db: Optional database session
        Returns:
            list of created Account ORM objects
        """
        return self.repo.bulk_create(accounts_data, user_id, db)
    
    def update_balance(self, account_id: str, val: float, db: Session = None):
        """
        Updates account balance.
        Args:
            account_id: ID of account to update
            val: New balance value
            db: Optional database session
        Returns:
            Updated account object
        """
        return self.repo.update_balance(account_id, val, db)

    def get_by_id(self, account_id: str, db: Session = None) -> dict:
        """
        Gets account by account id.
        Args:
            account_id: Account ID
            db: Optional database session
        Returns:
            Account object
        """
        return self.repo.get_by_id(account_id, db)

    def get_by_user_id(self, user_id: str, db: Session = None) -> list[dict]:
        """
        Gets all accounts for specified user.
        Args:
            user_id: User ID to filter accounts
            db: Optional database session
        Returns:
            List of account dictionaries
        """
        return [a.to_dict() for a in self.repo.get_by_user_id(user_id, db)]


account_service = AccountService(repository=AccountRepository())