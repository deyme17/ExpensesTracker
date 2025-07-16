from abc import ABC, abstractmethod


class BaseWebHookService(ABC):
    """
    Abstract base class for webhook services.
    """
    @abstractmethod
    def save_hooked_transactions(self, data: dict) -> None:
        """
        Abstract method that should handle incoming webhook data
        and save transactions accordingly.
        """
        pass
