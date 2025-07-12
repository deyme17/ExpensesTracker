import numpy as np
from kivy.properties import ListProperty
from app.utils.helpers import set_bins
from app.models.graphs.base_graph import BaseGraph


class DistributionGraph(BaseGraph):
    """
    Histogram model of transaction amounts.
    """
    transactions = ListProperty([])

    def fit(self, transactions):
        amounts = [abs(tx.amount) for tx in transactions]

        if not amounts:
            return [], []

        counts, bins = np.histogram(amounts, bins=set_bins(len(transactions)))
        centers = [(bins[i] + bins[i + 1]) / 2 for i in range(len(counts))]
        return centers, counts