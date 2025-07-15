from sqlalchemy.orm import Session
from typing import Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.category import CategoryORM
from app.models.category import Category


class CategoryRepository(BaseRepository[CategoryORM]):
    def __init__(self, session: Session):
        super().__init__(session, CategoryORM)