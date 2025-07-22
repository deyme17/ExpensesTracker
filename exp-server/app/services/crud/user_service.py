from app.database.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session


class UserService:
    """
    Service layer for user operations.
    Args:
        repository: UserRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def get_user_by_email(self, email: str, db: Session = None):
        """
        Retrieves user by email address.
        Args:
            email: User's email address
            db: Optional database session
        Returns:
            User object or None if not found
        """
        return self.repo.get_user_by_email(email, db)

    def get_user_by_id(self, user_id: str, db: Session = None):
        """
        Retrieves user by unique identifier.
        Args:
            user_id: User's unique ID
            db: Optional database session
        Returns:
            User data object or None if not found
        """
        return self.repo.get_user_by_id(user_id, db)
    
    def get_user_by_account_id(self, account_id: str, db: Session = None):
        """
        Retrieves user by unique account identifier.
        Args:
            account: Account's unique ID
            db: Optional database session
        Returns:
            User data object or None if not found
        """
        return self.repo.get_user_by_account_id(account_id, db)
    
    def create_user(self, user_data: dict, db: Session = None):
        """Creates a new user in the database.
        Args:
            user_data: Dictionary containing user attributes:
            db: Optional database session
        Returns:
            User: The created User ORM object
        """
        return self.repo.create_user(user_data, db)

user_service = UserService(repository=UserRepository())