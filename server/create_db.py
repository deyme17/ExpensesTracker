# server/create_db.py

from server.database.db import Base, engine
from server.models import user, transaction, category

# Створення таблиць
Base.metadata.create_all(bind=engine)
print("✅ Таблиці створено")
