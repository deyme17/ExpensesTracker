# server/models/user.py
<<<<<<< HEAD
from server.database.db import Base
from sqlalchemy import Column, String, DECIMAL

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    balance = Column(DECIMAL(19, 4))
=======
from sqlalchemy import Column, String, DECIMAL
from server.database.db import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    balance = Column(DECIMAL(19, 4), nullable=False)
>>>>>>> 9765729 (completed api)
