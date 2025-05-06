import hashlib
from uuid import uuid4
from kivy.clock import Clock
from app.models.user import User
from app.models.transaction import Transaction
from app.services.bank_services.monobank_service import MonobankService
from app.services.encryption_service import EncryptionService
from app.utils.validators import (
    validate_email,
    validate_password,
    validate_monobank_token
)

class AuthService:
    def __init__(self, storage_service):
        self.storage_service = storage_service
        self.current_user = None

    def is_authenticated(self):
        if self.current_user:
            return True
        user = self.storage_service.get_user()
        if user:
            self.current_user = user
            return True
        return False

    def get_current_user(self):
        if not self.current_user:
            self.current_user = self.storage_service.get_user()
        return self.current_user

    def logout(self):
        self.current_user = None
        self.storage_service.clear_user()
        return True

    def login(self, email, password, callback=None):
        if not email or not password:
            if callback:
                callback(False, "Будь ласка, введіть email і пароль")
            return False

        def authenticate(dt):
            try:
                user = self.storage_service.get_user()
                if not user or user.email != email.strip():
                    if callback:
                        callback(False, "Користувача не знайдено або email невірний")
                    return False

                if not user.check_password(password):
                    if callback:
                        callback(False, "Невірний пароль")
                    return False

                self.current_user = user
                if callback:
                    callback(True, "Успішний вхід")
                return True

            except Exception as e:
                if callback:
                    callback(False, f"Помилка входу: {str(e)}")
                return False

        Clock.schedule_once(authenticate, 1)
        return True

    def register(self, email, password, confirm_password, monobank_token, callback=None):
        if not validate_email(email):
            if callback:
                callback(False, "Некоректний email")
            return False

        is_valid, message = validate_password(password)
        if not is_valid:
            if callback:
                callback(False, message)
            return False

        if password != confirm_password:
            if callback:
                callback(False, "Паролі не співпадають")
            return False

        def process_registration(dt):
            try:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                raw_token = monobank_token.strip()

                if not validate_monobank_token(raw_token):
                    if callback:
                        callback(False, "Невірний формат токену Монобанк")
                    return False

                mono_service = MonobankService(token=raw_token)
                client_info = mono_service.get_client_info()

                user = User(
                    user_id=client_info["user_id"],
                    name=client_info["name"],
                    email=email,
                    balance=client_info["balance"],
                    token=raw_token,
                    password_hash=password_hash
                )

                self.current_user = user
                self.storage_service.save_user(user)

                transactions_data = mono_service.get_transactions(days=90)
                transactions = [Transaction.from_dict(t) for t in transactions_data]
                self.storage_service.save_transactions(transactions)

                if callback:
                    callback(True, "Реєстрація успішна")
                return True

            except Exception as e:
                if callback:
                    callback(False, f"{str(e)}")
                return False

        Clock.schedule_once(process_registration, 1.5)
        return True
