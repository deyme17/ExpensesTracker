from sqlalchemy import Column, String
from app.database.orm_models.base_orm import Base


class UserORM(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True) 
    name = Column(String, nullable=False) 
    email = Column(String, nullable=False) 
    encrypted_token = Column(String, nullable=False) 