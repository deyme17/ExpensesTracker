from server.database.repositories.account_repository import AccountRepository


class AccountService:
    """
    Service layer for account operations.
    Args:
        repository: AccountRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def create(self, data: dict):
        """
        Creates a new account.
        Args:
            data: Account data dictionary
        Returns:
            Created account object
        """
        return self.repo.create(data)
    
    def bulk_create(self, accounts_data: list[dict], user_id: str):
        """
        Bulk create accounts.
        Args:
            accounts_data: list of account dicts from банк-сервісу
            user_id: user id to link accounts to
        Returns:
            list of created Account ORM objects
        """
        return self.repo.bulk_create(accounts_data, user_id)
    
    def update_balance(self, account_id: str, val: float):
        """
        Updates account balance.
        Args:
            account_id: ID of account to update
            val: New balance value
        Returns:
            Updated account object
        """
        return self.repo.update_balance(account_id, val)

    def get_by_user_id(self, user_id: str) -> list[dict]:
        """
        Gets all accounts for specified user.
        Args:
            user_id: User ID to filter accounts
        Returns:
            List of account dictionaries
        """
        return [a.to_dict() for a in self.repo.get_by_user_id(user_id)]


account_service = AccountService(repository=AccountRepository())