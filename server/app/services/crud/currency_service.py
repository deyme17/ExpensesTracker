from app.database.repositories.currency_repository import CurrencyRepository
from sqlalchemy.orm import Session


class CurrencyService:
    """
    Service layer for currency operations.
    Args:
        repository: CurrencyRepository instance for data access
    """
    def __init__(self, repository):
        self.repo = repository

    def get_all(self, db: Session = None) -> list[dict]:
        """
        Retrieves all available currencies.
        Args:
            db: Optional database session
        Returns:
            List of currency dictionaries
        """
        try:
            currencies = self.repo.get_all(db)
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