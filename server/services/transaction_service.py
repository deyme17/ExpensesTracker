from server.database.repositories.transaction_repository import TransactionRepository

repo = TransactionRepository()

def get_all_by_user(user_id):
    return [t.__dict__ for t in repo.get_all_by_user(user_id)]

def create(data):
    return repo.create(data)

def delete(transaction_id):
    return repo.delete(transaction_id)

def update(transaction_id, data):
    return repo.update(transaction_id, data)