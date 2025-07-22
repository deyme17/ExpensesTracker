from sqlalchemy import Column, String, Integer
from app.database.orm_models.base_orm import Base
from app.utils.constants import DEFAULT_CATEGORY, DEFAULT_MCC


class CategoryORM(Base):
    __tablename__ = "categories"

    mcc_code = Column(Integer, primary_key=True, default=DEFAULT_MCC)
    name = Column(String, default=DEFAULT_CATEGORY)