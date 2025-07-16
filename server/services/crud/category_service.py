from server.database.repositories.category_repository import CategoryRepository


class CategoryService:
    """
    Service layer for category operations.
    Args:
        repository: CategoryRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def get_all(self) -> list[dict]:
        """
        Retrieves all available categories.
        Returns:
            List of category dictionaries
        """
        return [c.to_dict() for c in self.repo.get_all()]
    
    def get_existing_mcc_codes(self) -> set[int]:
        """
        Retrieves all existing MCC codes.
        Returns:
            Set of integer MCC codes
        """
        return {c.mcc_code for c in self.repo.get_all()}


category_service = CategoryService(repository=CategoryRepository())