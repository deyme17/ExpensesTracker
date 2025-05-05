from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.formatters import format_amount


class DistributionGraph(BaseGraphWidget):
    """
    Histogram of the distribution of transaction amounts.
    """

    def fit(self, transactions):
        amounts = [t.amount for t in transactions if not getattr(self, 'category', None) or t.category == self.category]

        if not amounts:
            return []

        bin_size = max(amounts) / 5 or 1
        bins = {}
        for amt in amounts:
            index = int(amt // bin_size) * bin_size
            bins[index] = bins.get(index, 0) + 1

        sorted_bins = sorted(bins.items())
        return [(format_amount(k), v) for k, v in sorted_bins]
