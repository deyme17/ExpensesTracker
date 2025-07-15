from server.database.repositories.base_repository import BaseRepository
from server.database.orm_models.category import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    def get_category_by_mcc(self, mcc_code: int):
        with self.get_session() as db:
            return db.query(Category).filter(Category.mcc_code == mcc_code).first()