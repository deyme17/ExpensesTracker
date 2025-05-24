from server.database.db import SessionLocal
from server.models.user import User
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def get_user_by_email(self, email: str):
        with SessionLocal() as db:
            return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str):
        with SessionLocal() as db:
            return db.query(User).filter(User.user_id == user_id).first()

    def create_user(self, data: dict, db=None):
        use_db = db or self.db
        try:
            user = User(**data)
            use_db.add(user)
            use_db.flush()
            return user
        except Exception:
            use_db.rollback()
            raise
