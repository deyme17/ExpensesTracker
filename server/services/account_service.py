from server.database.repositories.account_repository import AccountRepository


class AccountService:
    def __init__(self):
        self.repo = AccountRepository()

    def create(self, data):
        return self.repo.create(data)

    def get_by_user_id(self, user_id):
        return [a.to_dict() for a in self.repo.get_by_user_id(user_id)]

account_service = AccountService()