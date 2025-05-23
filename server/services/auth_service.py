from datetime import timedelta
from server.database.repositories.user_repository import UserRepository
from server.utils.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, data: dict):
        existing = self.repo.get_user_by_email(data["email"])
        if existing:
            raise Exception("User with such email already exists")

        user_data = {
            "user_id": data.get("user_id"),
            "name": data.get("name"),
            "email": data.get("email"),
            "hashed_password": hash_password(data["password"]),
            "encrypted_token": data.get("encrypted_token", "-")
        }

        user = self.repo.create_user(user_data)
        return user

    def login_user(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise Exception("Invalid password")

        token = create_access_token({"user_id": user.user_id}, expires_delta=timedelta(days=1))

        return {
            "token": token,
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "password_hash": user.hashed_password
        }