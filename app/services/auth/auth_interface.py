from app.services.auth.local_auth_service import LocalAuthService
from app.services.auth.remote_auth_service import RemoteAuthService

class AuthService:
    def __init__(self, storage_service, use_api=True):
        self.service = RemoteAuthService(storage_service) if use_api else LocalAuthService(storage_service)

    def login(self, email, password, callback=None):
        return self.service.login(email, password, callback)

    def register(self, email, password, confirm_password, monobank_token, callback=None):
        return self.service.register(email, password, confirm_password, monobank_token, callback)

    def logout(self):
        return self.service.logout()

    def is_authenticated(self):
        return self.service.is_authenticated()

    def get_current_user(self):
        return self.service.get_current_user()