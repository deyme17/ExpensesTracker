from sqlalchemy.orm import Session
from typing import Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.category import CategoryORM
from app.models.category import Category


class CategoryRepository(BaseRepository[CategoryORM]):
    def __init__(self, session: Session):
        super().__init__(session, CategoryORM)

    def save_categories(self, categories: list[Category]):
        for cat in categories:
            orm = CategoryORM(
                mcc_code=cat.mcc_code,
                name=cat.name    
            )
            self.session.merge(orm)
        self.session.commit()

    def get_categories(self) -> list[Category]:
        orm_categories = self.session.query(CategoryORM).all()
        categories = [Category(
                mcc_code=cat.mcc_code,
                name=cat.name    
            ) for cat in orm_categories]
        return categories