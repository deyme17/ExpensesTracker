from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models import User, Account
from sqlalchemy.orm import Session


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str, db: Session = None):
        def operation(session: Session):
            return session.query(User).filter(User.email == email).first()
        return self._with_session(operation, db)

    def get_user_by_id(self, user_id: str, db: Session = None):
        def operation(session: Session):
            return session.query(User).filter(User.user_id == user_id).first()
        return self._with_session(operation, db)

    def get_user_by_account_id(self, account_id: str, db: Session = None):
        def operation(session: Session):
            return (
                session.query(User)
                .join(Account, User.user_id == Account.user_id)
                .filter(Account.account_id == account_id)
                .first()
            )
        return self._with_session(operation, db)

    def create_user(self, data: dict, db: Session = None):
        def operation(session: Session):
            try:
                user = User(**data)
                session.add(user)
                session.flush()
                return user
            except Exception:
                session.rollback()
                raise
        return self._with_session(operation, db)