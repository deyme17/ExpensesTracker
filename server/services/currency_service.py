from server.database.repositories.currency_repository import CurrencyRepository

class CurrencyService:
    def __init__(self):
        self.repo = CurrencyRepository()

    def get_all(self):
        return [c.to_dict() for c in self.repo.get_all()]

currency_service = CurrencyService()