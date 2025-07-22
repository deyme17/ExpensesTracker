from datetime import timedelta
from sqlalchemy.orm import Session

from app.database.orm_models import User
from app.services.bank_services.bank_service import BankService
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.encryption import Encryption as enc
from dotenv import load_dotenv
import os

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)


class AuthService:
    """
    Service for handling user registration and authentication.
    """
    def __init__(self, user_service, bank_service_cls: BankService, bank_sync_service):
        """
        Args:
            user_service: Service for user data operations
            bank_service_cls: Returns a bank service instance (e.g., MonobankService)
            bank_sync_service: Service to sync accounts and transactions from bank
        """
        self.user_service = user_service
        self.bank_service_cls = bank_service_cls
        self.bank_sync_service = bank_sync_service

    def register_user(self, data: dict[str, str], db: Session) -> dict[str, str]:
        """
        Registers a new user with bank-linked data.
        Args:
            data: Registration data containing 'email', 'password', 'encrypted_token'
            db: SQLAlchemy session object
        Returns:
            Dict with user_id, name, and email
        """
        monobank_token = data.get("monobank_token", "").strip()
        if not monobank_token:
            raise Exception("monobank_token_missing")

        bank = self.bank_service_cls(monobank_token)
        client_info = bank.get_client_info()
        user_id = client_info["user_id"]

        if self.user_service.repo.get_user_by_email(data["email"]):
            raise Exception("user_exists")

        try:
            with db.begin():
                user_data = {
                    "user_id": user_id,
                    "name": client_info.get("name"),
                    "email": data.get("email"),
                    "hashed_password": hash_password(data["password"]),
                    "encrypted_token": enc.encrypt(monobank_token)
                }
                user = self.user_service.repo.create_user(user_data, db)
                self.bank_sync_service.sync_user_data(bank, user_id, db)
                
                if WEBHOOK_URL:
                    bank.set_webhook(WEBHOOK_URL)

        except Exception as e:
            raise Exception(f"Registration failed: {e}")

        return {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }

    def login_user(self, email: str, password: str, db: Session = None) -> dict[str, str]:
        """
        Authenticates user and returns JWT.
        Args:
            email: User email
            password: Plaintext password
            db: Optional database session
        Returns:
            Dict with token and user info
        """
        user = self.user_service.repo.get_user_by_email(email, db=db)
        if not user or not verify_password(password, user.hashed_password):
            raise Exception("invalid_credentials")

        token = create_access_token(
            {"user_id": user.user_id},
            expires_delta=timedelta(days=1)
        )

        return {
            "token": token,
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }

    def create_token(self, user: User) -> str:
        """
        Creates a JWT token for a given user.
        Args:
            user: User ORM model
        Returns:
            JWT token string
        """
        return create_access_token({"user_id": user.user_id}, expires_delta=timedelta(days=20))