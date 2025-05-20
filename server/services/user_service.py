from server.database.repositories.user_repository import UserRepository
from server.utils.security import hash_password
<<<<<<< HEAD
from server.utils.security import create_access_token
=======
>>>>>>> 9765729 (completed api)

repo = UserRepository()

def register(data):
    if repo.get_by_email(data["email"]):
        raise Exception("Користувач з таким email вже існує")
    data["password"] = hash_password(data["password"])
<<<<<<< HEAD
    user = repo.create(data)
    token = create_access_token({"user_id": user.user_id})
    return user, token
=======
    return repo.create(data)
>>>>>>> 9765729 (completed api)
