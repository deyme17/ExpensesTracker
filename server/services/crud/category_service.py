from server.database.repositories.category_repository import CategoryRepository
from sqlalchemy.orm import Session


class CategoryService:
    """
    Service layer for category operations.
    Args:
        repository: CategoryRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def get_all(self, db: Session = None) -> list[dict]:
        """
        Retrieves all available categories.
        Args:
            db: Optional database session
        Returns:
            List of category dictionaries
        """
        return [c.to_dict() for c in self.repo.get_all(db)]
    
    def get_existing_mcc_codes(self, db: Session = None) -> set[int]:
        """
        Retrieves all existing MCC codes.
        Args:
            db: Optional database session
        Returns:
            Set of integer MCC codes
        """
        return {c.mcc_code for c in self.repo.get_all(db)}


category_service = CategoryService(repository=CategoryRepository())