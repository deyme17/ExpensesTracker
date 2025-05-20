from server.database.db import SessionLocal
from server.models.user import User
<<<<<<< HEAD
from sqlalchemy.exc import SQLAlchemyError
=======
>>>>>>> 9765729 (completed api)

class UserRepository:
    def __init__(self):
        self.db = SessionLocal()

<<<<<<< HEAD
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str):
        return self.db.query(User).filter(User.user_id == user_id).first()

    def create_user(self, data: dict):
        try:
            user = User(**data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
=======
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, data: dict):
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
>>>>>>> 9765729 (completed api)
