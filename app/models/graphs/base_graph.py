from abc import ABCMeta, abstractmethod
from kivy.uix.boxlayout import BoxLayout

class BaseGraphWidget(BoxLayout):
    """
    Abstract base class for graphic widgets.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def fit(self, transactions):
        """
        Process transactions and generate data for the graph.
        Args:
            Transactions: List of Transaction Objects
        """
        raise NotImplementedError("The class should implement the method fit(transactions)")
