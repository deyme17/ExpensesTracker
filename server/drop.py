from sqlalchemy import text
from server.database.db import engine

def drop_transactions_table():
    with engine.connect() as conn:
        try:
            print("⏳ Видаляємо таблицю transactions...")
            conn.execute(text("DROP TABLE IF EXISTS transactions CASCADE;"))
            conn.commit()
            print("✅ Таблиця 'transactions' успішно видалена.")
        except Exception as e:
            print("❌ Помилка при видаленні:", str(e))

if __name__ == "__main__":
    drop_transactions_table()
