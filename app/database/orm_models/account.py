from sqlalchemy import Column, String, Float, Integer
from app.database.orm_models.base_orm import Base


class AccountORM(Base):
    __tablename__  = "accounts"

    account_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    currency_code = Column(Integer, nullable=False)
    balance = Column(Float, default=0.0)
    masked_pan = Column(String, nullable=False)