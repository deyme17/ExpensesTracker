from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.category import Category
from sqlalchemy.orm import Session


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    def get_category_by_mcc(self, mcc_code: int, db: Session = None):
        with self.get_session(db) as session:
            return session.query(Category).filter(Category.mcc_code == mcc_code).first()