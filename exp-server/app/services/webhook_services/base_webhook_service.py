from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class BaseWebHookService(ABC):
    """
    Abstract base class for webhook services.
    """
    @abstractmethod
    def save_hooked_transactions(self, data: dict, db: Session = None) -> None:
        """
        Abstract method that should handle incoming webhook data
        and save transactions accordingly.
        """
        pass
