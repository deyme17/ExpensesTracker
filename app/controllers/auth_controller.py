from kivy.clock import Clock
from app.services.auth.auth_interface import AuthService

class AuthController:
    def __init__(self, storage_service):
        self.auth_service = AuthService(storage_service)

    def login(self, email, password, callback=None):
        return self.auth_service.login(email, password, callback)

    def register(self, email, password, confirm_password, monobank_token, callback=None):
        return self.auth_service.register(email, password, confirm_password, monobank_token, callback)

    def logout(self):
        return self.auth_service.logout()

    def is_authenticated(self):
        return self.auth_service.is_authenticated()

    def get_current_user(self):
        return self.auth_service.get_current_user()