from sqlalchemy.orm import Session
from typing import Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.transaction import TransactionORM
from app.models.transaction import Transaction


class TransactionRepository(BaseRepository[TransactionORM]):
    def __init__(self, session: Session):
        super().__init__(session, TransactionORM)

    def save_transactions(self, transactions: list[Transaction]) -> None:
        if not transactions:
            return None
        for trx in transactions:
            orm_transaction = TransactionORM(
                transaction_id=trx.transaction_id,
                user_id=trx.user_id,
                amount=trx.amount,
                date=trx.date,
                account_id=trx.account_id,
                type=trx.type,
                mcc_code=trx.mcc_code,
                currency_code=trx.currency_code,
                description=trx.description,
                payment_method=trx.payment_method,
                cashback=trx.cashback,
                commission=trx.commission,
                is_synced=trx.is_synced,
            )
            self.session.merge(orm_transaction)
        self.session.commit()

    def get_transactions(self, user_id: Optional[str] = None) -> list[Transaction]:
        query = self.session.query(TransactionORM)
        if user_id:
            query = query.filter(TransactionORM.user_id == user_id)
        orm_transactions = query.all()
        return [
            Transaction(
                transaction_id=orm_trx.transaction_id,
                user_id=orm_trx.user_id,
                amount=orm_trx.amount,
                date=orm_trx.date,
                account_id=orm_trx.account_id,
                type=orm_trx.type,
                mcc_code=orm_trx.mcc_code,
                currency_code=orm_trx.currency_code,
                description=orm_trx.description,
                payment_method=orm_trx.payment_method,
                cashback=orm_trx.cashback,
                commission=orm_trx.commission,
                is_synced=orm_trx.is_synced
            )
            for orm_trx in orm_transactions
        ]
    
    def add_transaction(self, transaction: Transaction) -> None:
        orm_transaction = TransactionORM(
            transaction_id=transaction.transaction_id,
            user_id=transaction.user_id,
            amount=transaction.amount,
            date=transaction.date,
            account_id=transaction.account_id,
            type=transaction.type,
            mcc_code=transaction.mcc_code,
            currency_code=transaction.currency_code,
            description=transaction.description,
            payment_method=transaction.payment_method,
            cashback=transaction.cashback,
            commission=transaction.commission,
            is_synced=transaction.is_synced,
        )
        self.session.add(orm_transaction)
        self.session.commit()

    def update_transaction(self, transaction: Transaction) -> Optional[Transaction]:
        orm_trx = self.session.query(TransactionORM).filter(TransactionORM.transaction_id == transaction.transaction_id).first()
        if not orm_trx:
            return None
        # update all fields
        orm_trx.amount = transaction.amount
        orm_trx.date = transaction.date
        orm_trx.account_id = transaction.account_id
        orm_trx.type = transaction.type
        orm_trx.mcc_code = transaction.mcc_code
        orm_trx.currency_code = transaction.currency_code
        orm_trx.description = transaction.description
        orm_trx.payment_method = transaction.payment_method
        orm_trx.cashback = transaction.cashback
        orm_trx.commission = transaction.commission
        orm_trx.is_synced = transaction.is_synced

        self.session.commit()
        self.session.refresh(orm_trx)
        return transaction

    def delete_transaction(self, transaction_id: str) -> None:
        orm_transaction = self.session.query(TransactionORM).filter(TransactionORM.transaction_id == transaction_id).first()
        if orm_transaction:
            self.session.delete(orm_transaction)
            self.session.commit()

    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        orm_trx = self.session.query(TransactionORM).filter(TransactionORM.transaction_id == transaction_id).first()
        if not orm_trx:
            return None
        return Transaction(
            transaction_id=orm_trx.transaction_id,
            user_id=orm_trx.user_id,
            amount=orm_trx.amount,
            date=orm_trx.date,
            account_id=orm_trx.account_id,
            type=orm_trx.type,
            mcc_code=orm_trx.mcc_code,
            currency_code=orm_trx.currency_code,
            description=orm_trx.description,
            payment_method=orm_trx.payment_method,
            cashback=orm_trx.cashback,
            commission=orm_trx.commission,
            is_synced=orm_trx.is_synced
        )