from server.database.repositories.base_repository import BaseRepository
from server.database.orm_models.user import User
from server.database.db import SessionLocal


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str):
        with self.get_session() as db:
            return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str):
        with self.get_session() as db:
            return db.query(User).filter(User.user_id == user_id).first()

    def create_user(self, data: dict, db=None):
        use_db = db or SessionLocal()
        try:
            user = User(**data)
            use_db.add(user)
            use_db.flush()
            return user
        except Exception:
            use_db.rollback()
            raise