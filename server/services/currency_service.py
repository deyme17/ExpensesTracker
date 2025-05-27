from server.database.repositories.currency_repository import CurrencyRepository

class CurrencyService:
    def __init__(self):
        self.repo = CurrencyRepository()

    def get_all(self):
        try:
            currencies = self.repo.get_all()
            result = []
            for currency in currencies:
                try:
                    currency_dict = currency.to_dict()
                    result.append(currency_dict)
                except Exception as e:
                    print(f"[CurrencyService] Error processing currency {currency.__dict__}: {str(e)}")
                    continue
            print(f"[CurrencyService] Returning {len(result)} currencies")
            return result
        except Exception as e:
            print(f"[CurrencyService] Error fetching currencies: {str(e)}")
            raise

currency_service = CurrencyService()