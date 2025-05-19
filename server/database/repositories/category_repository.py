from server.database.db import SessionLocal
from server.models.category import Category
from sqlalchemy.exc import SQLAlchemyError

class CategoryRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_categories(self):
        return self.db.query(Category).all()

    def get_category_by_mcc(self, mcc_code: int):
        return self.db.query(Category).filter(Category.mcc_code == mcc_code).first()

    def create_category(self, mcc_code: int, name: str):
        try:
            category = Category(mcc_code=mcc_code, name=name)
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)
            return category
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_category(self, mcc_code: int):
        category = self.get_category_by_mcc(mcc_code)
        if category:
            try:
                self.db.delete(category)
                self.db.commit()
                return True
            except SQLAlchemyError as e:
                self.db.rollback()
                raise e
        return False
