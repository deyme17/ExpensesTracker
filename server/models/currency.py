from sqlalchemy import Column, BigInteger, String
from server.database.db import Base

class Currency(Base):
    __tablename__ = "currency"

    currency_code = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
<<<<<<< HEAD

=======
>>>>>>> 9765729 (completed api)
