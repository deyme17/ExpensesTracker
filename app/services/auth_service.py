from typing import Optional, Callable
from app.models.user import User
from app.api import api_register, api_login
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
from app.utils.token_exp import is_token_expired
from kivy.clock import Clock


class AuthService:
    """
    Handles user authentication and session management.
    Args:
        local_storage: Storage handler for user persistence
        data_loader: Component responsible for loading user data
        account_service: Service for managing user accounts
        transaction_service: Service for managing user transactions
    """
    def __init__(self, local_storage, data_loader, account_service, transaction_service):
        self.local_storage = local_storage
        self.data_loader = data_loader
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.current_user: Optional[User] = None

    def on_user_authenticated(self, user: User, callback: Optional[Callable[[], None]] = None) -> None:
        """
        Handle successful user authentication.
        Args:
            user: Authenticated user object
            callback: Optional callback to execute after authentication
        """
        self.current_user = user
        self.local_storage.user.save_user(user)
        
        # set user in storage
        self.local_storage.settings.set_current_user_id(user.user_id)

        # update user_id in services
        self.account_service.user_id = user.user_id
        self.transaction_service.user_id = user.user_id
        self.transaction_service.local_storage = self.local_storage

        self.data_loader.load_data(user, callback=callback)

    def is_authenticated(self) -> bool:
        """
        Check if a user is currently authenticated.
        Returns:
            True if user session exists and token is valid
        """
        if self.current_user:
            if is_token_expired(self.current_user.token):
                self.logout()
                return False
            return True
        
        # try to get current user from storage
        current_user_id = self.local_storage.settings.get_current_user_id()
        if current_user_id:
            user = self.local_storage.user.get_user(current_user_id)
            if user:
                if is_token_expired(user.token):
                    self.logout()
                    return False
                self.current_user = user
                return True
        
        return False

    def get_current_user(self) -> Optional[User]:
        """
        Retrieve the currently authenticated user.
        Returns:
            The authenticated user object or None
        """
        if not self.current_user:
            current_user_id = self.local_storage.settings.get_current_user_id()
            if current_user_id:
                self.current_user = self.local_storage.user.get_user(current_user_id)
        return self.current_user

    def logout(self) -> bool:
        """
        Terminate the current user session.
        Returns:
            Always returns True
        """
        if self.current_user:
            self.local_storage.user.clear_user(self.current_user.user_id)
        
        self.current_user = None
        self.local_storage.settings.clear_current_user()
        return True

    def _try_offline_login(self, email: str, callback: Optional[Callable[[bool, str], None]] = None) -> bool:
        """
        Attempt to authenticate the user offline using locally stored credentials.
        Args:
            email: User email address to verify against local data
            callback: Optional callback(success: bool, message: str) to notify about the result
        Returns:
            True if offline login succeeded, False otherwise
        """
        current_user_id = self.local_storage.settings.get_current_user_id()
        if not current_user_id:
            return False

        local_user = self.local_storage.user.get_user(current_user_id)
        if local_user and local_user.email == email:
            self.on_user_authenticated(
                local_user,
                callback=lambda: callback(True, LM.message("login_success_offline")) if callback else None
            )
            return True
        return False
    
    def login(self, email: str, password: str, callback: Optional[Callable[[bool, str], None]] = None) -> None:
        """
        Authenticate a user with email/password credentials.
        Args:
            email: User email address
            password: Plaintext password
            callback: Optional callback(success: bool, message: str)
        """
        def try_login(dt):
            try:
                response = api_login({"email": email, "password": password})

                if response.get("success"):
                    user = User.from_api_dict(response)
                    self.on_user_authenticated(
                        user, 
                        callback=lambda: callback(True, LM.message("login_success")) if callback else None
                    )
                else:
                    if not self._try_offline_login(email, callback):
                        error_code = response.get("error", ErrorCodes.UNKNOWN_ERROR)
                        if callback:
                            callback(False, LM.server_error(error_code))

            except Exception:
                if not self._try_offline_login(email, callback):
                    if callback:
                        callback(False, LM.server_error(ErrorCodes.UNKNOWN_ERROR))

        Clock.schedule_once(try_login, 0.5)

    def register(self, email: str, password: str, confirm_password: str, monobank_token: str, 
                callback: Optional[Callable[[bool, str], None]] = None) -> None:
        """
        Register a new user account.
        Args:
            email: User email address
            password: Plaintext password
            confirm_password: Password confirmation
            token: Monobank API token
            callback: Optional callback(success: bool, message: str)
        """
        def try_register(dt):
            try:
                payload = {
                    "email": email,
                    "password": password,
                    "monobank_token": monobank_token
                }
                print("REGISTRATION")
                response = api_register(payload)
                print(response)
                
                if response.get("success"):
                    user = User.from_api_dict(response)
                    self.local_storage.user.save_user(user)
                    self.current_user = user
                    
                    # set current user in storage
                    self.local_storage.settings.set_current_user_id(user.user_id)
                    
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