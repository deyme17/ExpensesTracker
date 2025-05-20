from server.database.repositories.category_repository import CategoryRepository

repo = CategoryRepository()

def get_all():
<<<<<<< HEAD
    return [c.__dict__ for c in repo.get_all()]
=======
    return [c.__dict__ for c in repo.get_all()]

>>>>>>> 9765729 (completed api)
