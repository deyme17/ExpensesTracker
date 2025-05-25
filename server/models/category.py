from sqlalchemy import Column, BigInteger, String
from server.database.db import Base

class Category(Base):
    __tablename__ = "categories"
    mcc_code = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "mcc_code": self.mcc_code,
            "name": self.name
        }