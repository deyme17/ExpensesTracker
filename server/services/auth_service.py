from datetime import timedelta, datetime
from server.database.db import SessionLocal
from server.services.bank_services.monobank_service import MonobankService
from server.services.user_service import UserService
from server.services.account_service import AccountService
from server.services.transaction_service import TransactionService
from server.models.user import User
from server.models.category import Category
from server.utils.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self):
        self.user_service = UserService()
        self.account_service = AccountService()
        self.transaction_service = TransactionService()

    def register_user(self, data: dict):
        token = data.get("encrypted_token", "").strip()
        if not token:
            raise Exception("token_missing")

        mono = MonobankService(token)
        client_info = mono.get_client_info()
        user_id = client_info["user_id"]

        with SessionLocal() as db:
            try:
                # email
                if self.user_service.repo.get_user_by_email(data["email"]):
                    raise Exception("user_exists")

                # user
                user_data = {
                    "user_id": user_id,
                    "name": client_info.get("name"),
                    "email": data.get("email"),
                    "hashed_password": hash_password(data["password"]),
                    "encrypted_token": token
                }
                user = self.user_service.repo.create_user(user_data, db)

                # accounts
                accounts_data = client_info.get("accounts", [])
                if not accounts_data:
                    raise Exception("no_accounts_found")

                accounts = self.account_service.repo.bulk_create(accounts_data, user_id, db)

                # transactions
                all_transactions = []
                for acc in accounts:
                    txs = mono.get_transactions(acc.account_id, days=31)
                    all_transactions.extend(self.transaction_service.map_transactions(txs, user_id, acc.account_id))

                # add categories
                existing_mcc = {c.mcc_code for c in db.query(Category).all()}
                missing_mcc = {t.mcc_code for t in all_transactions if t.mcc_code not in existing_mcc}
                for code in missing_mcc:
                    db.add(Category(mcc_code=code, name="other"))

                for tx in all_transactions:
                    db.add(tx)

                db.commit()

                return {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email
                }

            except Exception as e:
                db.rollback()
                raise e

    def login_user(self, email: str, password: str):
        user = self.user_service.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise Exception("invalid_credentials")

        token = create_access_token({"user_id": user.user_id}, expires_delta=timedelta(days=1))

        return {
            "token": token,
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }

    def get_user_by_id(self, user_id: str):
        user = self.user_service.repo.get_user_by_id(user_id)
        if not user:
            raise Exception("user_not_found")
        return user

    def create_token(self, user: User) -> str:
        return create_access_token({"user_id": user.user_id}, expires_delta=timedelta(days=1))