from app.utils.constants import (
    CHART_TYPE_HISTOGRAM, CHART_TYPE_PIE, CHART_TYPE_LINE
)
from app.models.graphs.distribution_graph import DistributionGraph
from app.models.graphs.share_graph import ShareGraph
from app.models.graphs.dynamics_graph import DynamicsGraph


class AnalyticsData:
    def __init__(self, stats, raw_transactions, transaction_type, start_date, end_date):
        self.stats = stats
        self.raw_transactions = raw_transactions
        self.transaction_type = transaction_type
        self.start_date = start_date
        self.end_date = end_date

        self._chart = {
            CHART_TYPE_HISTOGRAM: DistributionGraph(),
            CHART_TYPE_PIE: ShareGraph(),
            CHART_TYPE_LINE: DynamicsGraph()
        }

    def get_avg_value(self):
        return self.stats['avg']

    def get_min_value(self):
        return self.stats['min']

    def get_max_value(self):
        return self.stats['max']

    def get_total(self):
        return self.stats['total']

    def get_count(self):
        return self.stats['count']

    def get_top_category(self):
        return self.stats['top_category']

    def get_chart_data(self, chart_type):
        strategy = self._chart.get(chart_type)
        if not strategy:
            return []
        return strategy.fit(self.raw_transactions)
