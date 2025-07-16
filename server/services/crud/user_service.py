from server.database.repositories.user_repository import UserRepository


class UserService:
    """
    Service layer for user operations.
    Args:
        repository: UserRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def get_user_by_email(self, email: str) -> dict:
        """
        Retrieves user by email address.
        Args:
            email: User's email address
        Returns:
            User data dictionary or None if not found
        """
        return self.repo.get_user_by_email(email)

    def get_user_by_id(self, user_id: str) -> dict:
        """
        Retrieves user by unique identifier.
        Args:
            user_id: User's unique ID
        Returns:
            User data dictionary or None if not found
        """
        return self.repo.get_user_by_id(user_id)


user_service = UserService(repository=UserRepository())