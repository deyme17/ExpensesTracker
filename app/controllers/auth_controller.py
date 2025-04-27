from app.models.user import User
from app.utils.validators import validate_email, validate_password
from kivy.clock import Clock


class AuthController:
    def __init__(self, storage_service):
        """
        Init the authentication controller.
        
        Args:
            storage_service: Service for storing user data
        """
        self.storage_service = storage_service
        self.current_user = None
    
    def login(self, email, password, callback=None):
        """
        Authenticate a user with the provided credentials.
        
        Args:
            email: User's email address
            password: User's password
            callback: Function to call with result (success, message)
        """
        # validation
        if not email:
            if callback:
                callback(False, "Будь ласка, введіть email")
            return False
        
        if not password:
            if callback:
                callback(False, "Будь ласка, введіть пароль")
            return False
        
        def authenticate(dt):
            try:
                # TODO тут треба буде зробити перевірку через апі/бд
                if validate_email(email):
                    user = User(
                        user_id=f"user_{hash(email) % 10000}",
                        name=email.split('@')[0],
                        email=email,
                        balance=10000.0,
                        token=None
                    )
                    self.current_user = user
                    self.storage_service.save_user(user)
                    if callback:
                        callback(True, "Успішний вхід")
                    return True
                else:
                    if callback:
                        callback(False, "Невірний email або пароль")
                    return False
            except Exception as e:
                if callback:
                    callback(False, f"Помилка авторизації: {str(e)}")
                return False
        
        Clock.schedule_once(authenticate, 1)
        return True
    
    def register(self, email, password, confirm_password, monobank_token=None, callback=None):  # TODO
        """
        Register a new user with the provided information.
        
        Args:
            name: User's name
            email: User's email address
            password: User's password
            confirm_password: Password confirmation
            monobank_token: Optional MonoBank API token
            callback: Function to call with result (success, message)
        """
        # validation
        name=email.split('@')[0]
        
        if not email:
            if callback:
                callback(False, "Будь ласка, введіть email")
            return False
        
        if not validate_email(email):
            if callback:
                callback(False, "Будь ласка, введіть коректний email")
            return False
        
        if not password:
            if callback:
                callback(False, "Будь ласка, введіть пароль")
            return False
        
        if not validate_password(password):
            if callback:
                callback(False, "Пароль має бути не менше 6 символів")
            return False
        
        if password != confirm_password:
            if callback:
                callback(False, "Паролі не співпадають")
            return False
        
        def process_registration(dt):
            try:
                # TODO тут треба створити юзера в бд/апі
                user = User(
                    user_id=f"user_{hash(email) % 10000}",
                    name=name,
                    email=email,
                    balance=0.0,
                    token=monobank_token
                )
                self.current_user = user
                self.storage_service.save_user(user)
                
                if callback:
                    callback(True, "Реєстрація успішна")
                return True
            except Exception as e:
                if callback:
                    callback(False, f"Помилка реєстрації: {str(e)}")
                return False
        
        Clock.schedule_once(process_registration, 1.5)
        return True
    
    def logout(self):
        """Log out the current user."""
        self.current_user = None
        self.storage_service.clear_user()
        return True
    
    def is_authenticated(self):
        """Check if a user is currently authenticated."""
        if self.current_user:
            return True
        
        # try to get user from storage
        user = self.storage_service.get_user()
        if user:
            self.current_user = user
            return True
        
        return False
    
    def get_current_user(self):
        """Get the currently authenticated user."""
        if not self.current_user:
            self.current_user = self.storage_service.get_user()
        return self.current_user