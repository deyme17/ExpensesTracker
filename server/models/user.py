# server/models/user.py
from server.database.db import Base
from sqlalchemy import Column, String, DECIMAL

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    balance = Column(DECIMAL(19, 4))
