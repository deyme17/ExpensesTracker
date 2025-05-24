from server.database.db import engine, Base
from server.models import user, account, transaction, category, currency

def init():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init()