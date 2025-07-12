from abc import ABC, abstractmethod


class BaseGraph(ABC):
    """
    Abstract base class for graphs.
    """
    def __init__(self, renderer, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.renderer = renderer

    @abstractmethod
    def fit(self, transactions):
        """
        Process transactions and generate data for the graph.
        Args:
            transactions: List of Transaction Objects
        """
        raise NotImplementedError("The class should implement the method fit(transactions)")
    
    def render(self, transactions):
        """
        Fit the data and render the graph.
        Args:
            transactions: List of Transaction Objects
        """
        data = self.fit(transactions)
        if data:
            self.renderer._render(*data)