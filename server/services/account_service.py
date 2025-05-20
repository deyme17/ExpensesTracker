from server.database.repositories.account_repository import AccountRepository

repo = AccountRepository()

def create(data):
    return repo.create(data)
