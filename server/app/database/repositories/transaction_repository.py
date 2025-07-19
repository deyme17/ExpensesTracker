from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.transaction import Transaction
from sqlalchemy.orm import Session


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    def get_all_by_user(self, user_id: str, db: Session = None):
        with self.get_session(db) as session:
            return session.query(Transaction).filter(Transaction.user_id == user_id).all()