class AuthController:
    """
    Handles user authentication and session management operations.
    Args:
        auth_service: Service layer handling authentication logic and storage.
    """
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def login(self, email: str, password: str, callback=None):
        return self.auth_service.login(email, password, callback)

    def register(self, email: str, password: str, confirm_password: str, monobank_token: str, callback=None):
        return self.auth_service.register(email, password, confirm_password, monobank_token, callback)

    def logout(self) -> bool:
        return self.auth_service.logout()

    def is_authenticated(self) -> bool:
        return self.auth_service.is_authenticated()

    def get_current_user(self):
        return self.auth_service.get_current_user()