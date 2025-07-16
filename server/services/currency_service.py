from server.database.repositories.currency_repository import CurrencyRepository


class CurrencyService:
    """
    Service layer for currency operations.
    Args:
        repository: CurrencyRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def get_all(self) -> list[dict]:
        """
        Retrieves all available currencies.
        Returns:
            List of currency dictionaries
        """
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


currency_service = CurrencyService(repository=CurrencyRepository())