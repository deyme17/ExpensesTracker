from server.database.db import SessionLocal
from server.models.category import Category
from sqlalchemy.exc import SQLAlchemyError

class CategoryRepository:
    def get_all_categories(self):
        with SessionLocal() as db:
            return db.query(Category).all()

    def get_category_by_mcc(self, mcc_code: int):
        with SessionLocal() as db:
            return db.query(Category).filter(Category.mcc_code == mcc_code).first()