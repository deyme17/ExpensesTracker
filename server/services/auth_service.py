from datetime import timedelta

from server.database.db import SessionLocal
from server.services.bank_services.monobank_service import MonobankService
from server.services.crud import user_service, account_service, transaction_service
from server.database.orm_models import User, Category

from server.utils.security import hash_password, verify_password, create_access_token


class AuthService:
    """
    Handles user authentication, registration and token management.
    Args:
        user_service: Service for user data operations
        account_service: Service for account operations
        transaction_service: Service for transaction operations
        bank_service: Factory for bank API service (e.g. MonobankService)
    """
    def __init__(self, user_service, account_service, transaction_service, bank_service):
        self.user_service = user_service
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.bank_service = bank_service

    def register_user(self, data: dict[str, str]) -> dict[str, str]:
        """
        Registers a new user with linked bank account.
        Args:
            data: Registration data containing:
                - email: User email
                - password: Plaintext password
                - encrypted_token: Bank API token
        Returns:
            Dictionary with basic user info:
                - user_id: Unique user identifier
                - name: User's name from bank
                - email: User's email
        """
        token = data.get("encrypted_token", "").strip()
        if not token:
            raise Exception("token_missing")

        bank = self.bank_service(token)
        client_info = bank.get_client_info()
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
                    txs = bank.get_transactions(acc.account_id, days=31)
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

    def login_user(self, email: str, password: str) -> dict[str, str]:
        """
        Authenticates user and generates JWT token.
        Args:
            email: User's email address
            password: Plaintext password for verification
        Returns:
            Dictionary containing:
                - token: JWT access token
                - user_id: Authenticated user ID
                - name: User's name
                - email: User's email
        """
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

    def get_user_by_id(self, user_id: str) -> User:
        """
        Retrieves user by their unique identifier.
        Args:
            user_id: Unique user ID to lookup
        Returns:
            User ORM object with all user data
        """
        user = self.user_service.repo.get_user_by_id(user_id)
        if not user:
            raise Exception("user_not_found")
        return user

    def create_token(self, user: User) -> str:
        """Generates JWT token for authenticated user.
        Args:
            user: User ORM object to generate token for
        Returns:
            JWT token string valid for 1 day
        """
        return create_access_token({"user_id": user.user_id}, expires_delta=timedelta(days=20))
    

auth_service = AuthService(user_service=user_service, account_service=account_service, transaction_service=transaction_service, 
                           bank_service=MonobankService())