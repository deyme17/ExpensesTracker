from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models import User, Account
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
        
    def get_user_by_account_id(self, account_id: str, db: Session = None):
        with self.get_session(db) as session:
            return (
                session.query(User)
                .join(Account, User.user_id == Account.user_id)
                .filter(Account.account_id == account_id)
                .first()
            )

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