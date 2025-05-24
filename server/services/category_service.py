from server.database.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_all(self):
        return [c.__dict__ for c in self.repo.get_all_categories()]

category_service = CategoryService()