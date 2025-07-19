from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

home_dir = os.path.expanduser("~")
db_path = os.path.join(home_dir, ".expenses_tracker", "expenses_tracker.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)