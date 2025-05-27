from server.database.repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_user_by_email(self, email: str):
        return self.repo.get_user_by_email(email)

    def get_user_by_id(self, user_id: str):
        return self.repo.get_user_by_id(user_id)