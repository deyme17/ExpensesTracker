from sqlalchemy import Column, BigInteger, String
from server.database.db import Base

class Category(Base):
    __tablename__ = "category"

    mcc_code = Column(BigInteger, primary_key=True)
<<<<<<< HEAD
    name = Column(String(255), nullable=False)
=======
    name = Column(String(255), nullable=False)
>>>>>>> 9765729 (completed api)
