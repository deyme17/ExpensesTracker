from server.database.db import Base
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    encrypted_token = Column(String, nullable=False)