from abc import ABC, abstractmethod

class BaseTransactionService(ABC):
    @abstractmethod
    def add_transaction(self, **kwargs): ...

    @abstractmethod
    def update_transaction(self, transaction_id, **kwargs): ...

    @abstractmethod
    def delete_transaction(self, transaction_id): ...

    @abstractmethod
    def get_transaction_by_id(self, transaction_id): ...

    @abstractmethod
    def get_transactions(self, force_refresh=False): ...
