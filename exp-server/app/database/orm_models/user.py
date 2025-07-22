from app.database.db import Base
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    encrypted_token = Column(String, nullable=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "encrypted_token": self.encrypted_token,
        }