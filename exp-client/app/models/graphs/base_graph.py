from abc import ABC, abstractmethod


class BaseGraph(ABC):
    """
    Abstract base class for graphs.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    @abstractmethod
    def fit(self, transactions):
        """
        Process transactions and generate data for the graph.
        Args:
            transactions: List of Transaction Objects
        """
        raise NotImplementedError("The class should implement the method fit(transactions)")