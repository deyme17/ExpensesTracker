from kivy.clock import Clock
from app.models.user import User
from app.services.auth.auth_service import BaseAuthService
from app.services.api_service import api_register, api_login
from app.utils.language_mapper import LanguageMapper as LM

class RemoteAuthService(BaseAuthService):
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
        def try_login(dt):
            try:
                response = api_login({"email": email, "password": password})
                if response.get("success"):
                    user = User.from_api_dict(response)
                    self.storage_service.save_user(user)
                    self.current_user = user
                    if callback:
                        callback(True, LM.message("login_success"))
                else:
                    if callback:
                        callback(False, response.get("error", LM.message("login_error_generic")))
            except Exception as e:
                if callback:
                    callback(False, LM.message("login_error").format(error=str(e)))

        Clock.schedule_once(try_login, 0.5)

    def register(self, email, password, confirm_password, monobank_token, callback=None):
        # Validation left to caller or controller
        def try_register(dt):
            try:
                from app.services.bank_services.monobank_service import MonobankService
                mono = MonobankService(token=monobank_token.strip())
                client = mono.get_client_info()

                payload = {
                    "user_id": client["user_id"],
                    "name": client["name"],
                    "email": email,
                    "password": password,
                    "encrypted_token": monobank_token.strip()
                }

                response = api_register(payload)
                if response.get("success"):
                    user = User.from_api_dict(response)
                    self.storage_service.save_user(user)
                    self.current_user = user
                    if callback:
                        callback(True, LM.message("registration_success"))
                else:
                    if callback:
                        callback(False, response.get("error", LM.message("registration_error_generic")))
            except Exception as e:
                if callback:
                    callback(False, LM.message("registration_error").format(error=str(e)))

        Clock.schedule_once(try_register, 1)