from server.database.repositories.base_repository import BaseRepository
from server.database.orm_models.transaction import Transaction


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    def get_all_by_user(self, user_id: str):
        with self.get_session() as db:
            return db.query(Transaction).filter(Transaction.user_id == user_id).all()