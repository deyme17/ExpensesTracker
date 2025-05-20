<<<<<<< HEAD
# server/create_db.py

from server.database.db import Base, engine
from server.models import user, transaction, category

# Створення таблиць
Base.metadata.create_all(bind=engine)
print("✅ Таблиці створено")
=======
from server.database.db import Base, engine, SessionLocal
from server.models.user import User
from server.models.account import Account
from server.models.transaction import Transaction
from server.models.category import Category
from server.models.currency import Currency

def recreate_all():
    print("❌ Видаляємо старі таблиці...")
    Base.metadata.drop_all(bind=engine)
    print("📦 Створюємо нові таблиці...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблиці створено!")

    insert_initial_data()

def insert_initial_data():
    print("➕ Додаємо базові валюти й категорії...")
    db = SessionLocal()

    try:
        # Валюти
        currencies = [
            Currency(currency_code=980, name="UAH"),
            Currency(currency_code=840, name="USD"),
            Currency(currency_code=978, name="EUR"),
        ]
        db.add_all(currencies)

        # Категорії
        categories = [
            Category(mcc_code=5411, name="Продукти"),
            Category(mcc_code=5812, name="Ресторани"),
            Category(mcc_code=4111, name="Транспорт"),
        ]
        db.add_all(categories)

        db.commit()
        print("✅ Валюти та категорії додані.")
    except Exception as e:
        db.rollback()
        print("❌ Помилка при додаванні даних:", e)
    finally:
        db.close()

if __name__ == "__main__":
    recreate_all()
>>>>>>> 9765729 (completed api)
