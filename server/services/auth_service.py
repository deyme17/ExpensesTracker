from server.database.repositories.user_repository import UserRepository
from server.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from datetime import timedelta

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, data):
        existing = self.repo.get_user_by_email(data["email"])
        if existing:
            raise Exception("User already exists")

        hashed_pw = hash_password(data["password"])

        user_data = {
            "user_id": data["user_id"],
            "name": data["name"],
            "email": data["email"],
            "password": hashed_pw,
            "balance": 0,
        }

        return self.repo.create_user(user_data)

    def login_user(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)
        if not user:
            raise Exception("Invalid credentials")

        if not verify_password(password, user.password):
            raise Exception("Invalid credentials")

        token = create_access_token(
            {"user_id": user.user_id}, expires_delta=timedelta(days=1)
        )

        return {
            "token": token,
            "user_id": user.user_id,
            "name": user.name
        }
