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
    
    def update_balance(self, account_id: str, val: float):
        """
        Updates account balance.
        Args:
            account_id: ID of account to update
            val: New balance value
        Returns:
            Updated account object
        """
        return self.repo.update(account_id, val)

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