from server.database.repositories.user_repository import UserRepository
from server.utils.security import hash_password
from server.utils.security import create_access_token

repo = UserRepository()

def register(data):
    if repo.get_by_email(data["email"]):
        raise Exception("Користувач з таким email вже існує")
    data["password"] = hash_password(data["password"])
    user = repo.create(data)
    token = create_access_token({"user_id": user.user_id})
    return user, token
