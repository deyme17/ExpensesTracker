from server.database.repositories.base_repository import BaseRepository
from server.database.orm_models.user import User
from server.database.db import SessionLocal
from sqlalchemy.orm import Session


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str, db: Session = None):
        with self.get_session(db) as session:
            return session.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str, db: Session = None):
        with self.get_session(db) as session:
            return session.query(User).filter(User.user_id == user_id).first()

    def create_user(self, data: dict, db: Session = None):
        session = self.get_session(db)
        try:
            user = User(**data)
            session.add(user)
            session.flush()
            return user
        except Exception:
            session.rollback()
            raise