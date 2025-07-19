from sqlalchemy import Column, String, Integer
from app.database.orm_models.base_orm import Base
from app.utils.constants import DEFAULT_CURRENCY, DEFAULT_CURRENCY_CODE


class CurrencyORM(Base):
    __tablename__ = "currencies"

    currency_code = Column(Integer, primary_key=True, default=DEFAULT_CURRENCY_CODE)
    name = Column(String, default=DEFAULT_CURRENCY)