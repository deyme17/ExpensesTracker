from app.models.user import User
from app.services.api import api_register, api_login
from app.services.crud_services.account import AccountService
from app.services.crud_services.transaction import TransactionService
from app.services.crud_services.category import CategoryService
from app.services.crud_services.currency import CurrencyService
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
from kivy.clock import Clock

class AuthService:
    def __init__(self, storage_service):
        self.storage = storage_service
        self.current_user = None

    def is_authenticated(self):
        if self.current_user:
            return True
        user = self.storage.get_user()
        if user:
            self.current_user = user
            return True
        return False

    def get_current_user(self):
        if not self.current_user:
            self.current_user = self.storage.get_user()
        return self.current_user

    def logout(self):
        self.current_user = None
        self.storage.clear_user()
        return True

    def login(self, email, password, callback=None):
        def try_login(dt):
            try:
                response = api_login({"email": email, "password": password})
                if response.get("success"):
                    user = User.from_api_dict(response)
                    self.storage.save_user(user)
                    self.current_user = user
                    self._load_data(user, callback=lambda: callback(True, LM.message("login_success")) if callback else None)
                else:
                    local_user = self.storage.get_user()
                    if local_user and local_user.email == email:
                        self.current_user = local_user
                        self._load_data(local_user, callback=lambda: callback(True, LM.message("login_success_offline")) if callback else None)
                    else:
                        error_code = response.get("error", ErrorCodes.UNKNOWN_ERROR)
                        if callback:
                            callback(False, LM.server_error(error_code))
            except Exception as e:
                local_user = self.storage.get_user()
                if local_user and local_user.email == email:
                    self.current_user = local_user
                    self._load_data(local_user, callback=lambda: callback(True, LM.message("login_success_offline")) if callback else None)
                else:
                    if callback:
                        callback(False, LM.server_error(ErrorCodes.UNKNOWN_ERROR))

        Clock.schedule_once(try_login, 0.5)

    def register(self, email, password, confirm_password, token, callback=None):
        def try_register(dt):
            try:
                payload = {
                    "email": email,
                    "password": password,
                    "encrypted_token": token
                }
                print("REGISTRATION")
                response = api_register(payload)
                print(response)
                if response.get("success"):
                    user = User.from_api_dict(response)
                    self.storage.save_user(user)
                    self.current_user = user
                    def after_load():
                        if callback:
                            callback(True, LM.message("registration_success"))
                    self._load_data(user, callback=after_load)
                else:
                    error_code = response.get("error", ErrorCodes.UNKNOWN_ERROR)
                    if callback:
                        callback(False, LM.server_error(error_code))
            except Exception:
                if callback:
                    callback(False, LM.server_error(ErrorCodes.UNKNOWN_ERROR))
        Clock.schedule_once(try_register, 1)

    def _load_data(self, user, callback=None):
        try:
            from kivy.app import App
            app = App.get_running_app()

            app.transaction_controller.transaction_service = TransactionService(user_id=user.user_id, storage_service=self.storage)
            app.account_service.user_id = user.user_id

            app.account_service.get_accounts()
            app.transaction_controller.transaction_service.get_transactions(force_refresh=True)
            CategoryService(self.storage).get_categories()
            CurrencyService(self.storage).get_currencies()

            # set active account if exists
            accounts, _ = app.account_service.get_accounts()
            print("[AuthService] Accounts fetched:", accounts)
            if accounts:
                print("[AuthService] Setting active account:", accounts[-1].account_id)
                self.storage.set_active_account(accounts[-1].account_id)
            else:
                print("[AuthService] No accounts returned")


            print("[AuthService] Transactions loaded for:", user.user_id)

        except Exception as e:
            print(f"[AuthService] load data error: {e}")
        finally:
            if callback:
                Clock.schedule_once(lambda dt: callback(), 0.1)
