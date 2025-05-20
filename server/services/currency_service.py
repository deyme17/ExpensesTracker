from server.database.repositories.currency_repository import CurrencyRepository

repo = CurrencyRepository()

def get_all():
    return [c.__dict__ for c in repo.get_all()]