from app.models.user import User
from app.api import api_register, api_login
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
from kivy.clock import Clock


class AuthService:
    """
    Handles user authentication and session management.
    Args:
        storage_service: Storage handler for user persistence
        data_loader: Component responsible for loading user data
        account_service:
        transaction_service:
    """
    def __init__(self, storage_service, data_loader, account_service, transaction_service):
        self.storage = storage_service
        self.data_loader = data_loader
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.current_user = None

    def on_user_authenticated(self, user, callback=None):
        self.current_user = user
        self.storage.save_user(user)

        # update user_id
        self.account_service.user_id = user.user_id
        self.transaction_service.user_id = user.user_id
        self.transaction_service.storage = self.storage

        self.data_loader.load_data(user, callback=callback)

    def is_authenticated(self) -> bool:
        """
        Checks if a user is currently authenticated.
        Returns:
            bool: True if user session exists (checks storage if needed)
        """
        if self.current_user:
            return True
        user = self.storage.get_user()
        if user:
            self.current_user = user
            return True
        return False

    def get_current_user(self):
        """
        Retrieves the currently authenticated user.
        Returns:
            User: The authenticated user object or None
        """
        if not self.current_user:
            self.current_user = self.storage.get_user()
        return self.current_user

    def logout(self) -> bool:
        """
        Terminates the current user session.
        Returns:
            bool: Always returns True
        """
        self.current_user = None
        self.storage.clear_user()
        return True

    def login(self, email: str, password: str, callback=None):
        """
        Authenticates a user with email/password credentials.
        Args:
            email: User email address
            password: Plaintext password
            callback: Optional callback(status: bool, message: str)
        """
        def try_login(dt):
            try:
                response = api_login({"email": email, "password": password})

                if response.get("success"):
                    user = User.from_api_dict(response)
                    self.on_user_authenticated(user, callback=lambda: callback(True, LM.message("login_success")) if callback else None)
                else:
                    local_user = self.storage.get_user()

                    if local_user and local_user.email == email:
                        self.on_user_authenticated(local_user, callback=lambda: callback(True, LM.message("login_success_offline")) if callback else None)
                    else:
                        error_code = response.get("error", ErrorCodes.UNKNOWN_ERROR)
                        if callback:
                            callback(False, LM.server_error(error_code))

            except Exception:
                local_user = self.storage.get_user()
                if local_user and local_user.email == email:
                    self.on_user_authenticated(local_user, callback=lambda: callback(True, LM.message("login_success_offline")) if callback else None)
                else:
                    if callback:
                        callback(False, LM.server_error(ErrorCodes.UNKNOWN_ERROR))

        Clock.schedule_once(try_login, 0.5)

    def register(self, email: str, password: str, confirm_password: str, token: str, callback=None):
        """
        Registers a new user account.
        Args:
            email: User email address
            password: Plaintext password
            confirm_password: Password confirmation
            token: Monobank API token
            callback: Optional callback(status: bool, message: str)
        """
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
                    self.data_loader.load_data(user, callback=after_load)
                else:
                    error_code = response.get("error", ErrorCodes.UNKNOWN_ERROR)
                    if callback:
                        callback(False, LM.server_error(error_code))
            except Exception:
                if callback:
                    callback(False, LM.server_error(ErrorCodes.UNKNOWN_ERROR))
                    
        Clock.schedule_once(try_register, 1)
