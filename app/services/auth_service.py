import hashlib
from uuid import uuid4
from kivy.clock import Clock
from datetime import datetime

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.services.bank_services.monobank_service import MonobankService
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.constants import MCC_MAPPING, CURRENCY_CODE_MAPPING
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
                callback(False, LM.message("missing_credentials"))
            return False

        def authenticate(dt):
            try:
                user = self.storage_service.get_user()
                if not user or user.email != email.strip():
                    if callback:
                        callback(False, LM.message("user_not_found"))
                    return False

                if not user.check_password(password):
                    if callback:
                        callback(False, LM.message("invalid_password"))
                    return False

                self.current_user = user
                if callback:
                    callback(True, LM.message("login_success"))
                return True

            except Exception as e:
                if callback:
                    callback(False, LM.message("login_error").format(error=str(e)))
                return False

        Clock.schedule_once(authenticate, 1)
        return True

    def register(self, email, password, confirm_password, monobank_token, callback=None):
        if not validate_email(email):
            if callback:
                callback(False, LM.message("invalid_email"))
            return False

        is_valid, message = validate_password(password)
        if not is_valid:
            if callback:
                callback(False, message)
            return False

        if password != confirm_password:
            if callback:
                callback(False, LM.message("password_mismatch"))
            return False

        Clock.schedule_once(lambda dt: self._process_registration(email, password, monobank_token, callback), 1.5)
        return True

    def _process_registration(self, email, password, monobank_token, callback):
        try:
            user = self._create_user(email, password, monobank_token)
            self.storage_service.save_user(user)
            self.current_user = user

            accounts = self._import_accounts(user)
            self.storage_service.save_accounts(accounts)

            active_account_id = self._select_active_account(accounts)
            self.storage_service.set_active_account(active_account_id)

            transactions = self._import_transactions(user.user_id, accounts)
            self.storage_service.save_transactions(transactions)

            if callback:
                callback(True, LM.message("registration_success"))
            return True
        except Exception as e:
            if callback:
                callback(False, LM.message("registration_error").format(error=str(e)))
            return False

    def _create_user(self, email, password, token):
        if not validate_monobank_token(token):
            raise ValueError(LM.message("invalid_token_format"))

        mono = MonobankService(token=token.strip())
        client = mono.get_client_info()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return User(
            user_id=client["user_id"],
            name=client["name"],
            email=email,
            password_hash=password_hash,
            token=token
        )

    def _import_accounts(self, user):
        mono = MonobankService(token=user.token)
        accounts_data = mono.get_client_info()["accounts"]
        return [Account.from_monobank_dict(acc, user.user_id) for acc in accounts_data]

    def _select_active_account(self, accounts):
        uah_accounts = [a for a in accounts if a.currency_code == 980]
        return (uah_accounts[0] if uah_accounts else accounts[0]).account_id

    def _import_transactions(self, user_id, accounts):
        mono = MonobankService(token=self.current_user.token)
        transactions = []
        for acc in accounts:
            data = mono.get_transactions(account_id=acc.account_id, days=31)
            transactions.extend([
                Transaction.from_monobank(t, user_id, acc.account_id)
                for t in data
            ])
        return transactions