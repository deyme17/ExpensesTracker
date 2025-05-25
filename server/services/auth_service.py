from datetime import datetime, timedelta
from server.database.repositories.user_repository import UserRepository
from server.utils.security import hash_password, verify_password, create_access_token
from server.database.db import SessionLocal
from server.models.user import User
from server.models.account import Account
from server.models.transaction import Transaction
from server.models.category import Category
from server.services.bank_services.monobank_service import MonobankService
from utils.language_mapper import LanguageMapper as LM
from sqlalchemy.exc import SQLAlchemyError

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, data: dict):
        with SessionLocal() as db:
            try:
                if self.repo.get_user_by_email(data["email"]):
                    raise Exception(LM.message("user_exists"))

                token = data.get("encrypted_token", "").strip()
                if not token:
                    raise Exception(LM.message("token_missing"))

                mono = MonobankService(token)
                client_info = mono.get_client_info()

                # user
                user_data = {
                    "user_id": client_info.get("user_id"),
                    "name": client_info.get("name"),
                    "email": data.get("email"),
                    "hashed_password": hash_password(data["password"]),
                    "encrypted_token": token
                }

                user = User(**user_data)
                db.add(user)
                db.flush()

                # accounts
                accounts_data = client_info.get("accounts", [])
                if not accounts_data:
                    raise Exception(LM.message("no_accounts_found"))

                accounts = [
                    Account(
                        account_id=a.get("id"),
                        user_id=user.user_id,
                        currency_code=a.get("currencyCode"),
                        balance=a.get("balance") / 100.0,
                        type=a.get("type", "default"),
                        masked_pan=a.get("maskedPan", [0])[0]
                    )
                    for a in accounts_data
                ]
                for acc in accounts:
                    db.add(acc)

                # transactions
                transactions = []
                for acc in accounts:
                    tx_data = mono.get_transactions(account_id=acc.account_id, days=31)
                    transactions += [
                        Transaction(
                            transaction_id=t.get("id"),
                            user_id=user.user_id,
                            amount=t.get("amount") / 100.0,
                            date=datetime.fromtimestamp(t.get("time")),
                            account_id=acc.account_id,
                            mcc_code=t.get("mcc", 0),
                            currency_code=t.get("currencyCode", 980),
                            payment_method="card",
                            description=t.get("description", ""),
                            cashback=t.get("cashbackAmount", 0) / 100.0,
                            commission=t.get("commissionRate", 0) / 100.0
                        ) for t in tx_data
                    ]

                # add mcc
                existing_codes = {c.mcc_code for c in db.query(Category).all()}
                missing_codes = {t.mcc_code for t in transactions if t.mcc_code not in existing_codes}
                for code in missing_codes:
                    db.add(Category(mcc_code=code, name="other"))

                for tx in transactions:
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
        user = self.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise Exception(LM.message("invalid_credentials"))

        token = create_access_token({"user_id": user.user_id}, expires_delta=timedelta(days=1))

        return {
            "token": token,
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }

    def get_user_by_id(self, user_id: str):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise Exception(LM.message("user_not_found"))
        return user

    def create_token(self, user: User) -> str:
        return create_access_token({"user_id": user.user_id}, expires_delta=timedelta(days=1))