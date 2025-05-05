from app.models.graphs.base_graph import BaseGraphWidget
from collections import defaultdict
from datetime import datetime


class DynamicsGraph(BaseGraphWidget):
    """
    Lineary graph of dynamics of changes by dates.
    """

    def fit(self, transactions):
        if not transactions:
            return []

        grouped = defaultdict(float)
        for t in transactions:
            if getattr(self, 'category', None) and t.category != self.category:
                continue
            date_str = t.date.strftime('%Y-%m-%d')
            grouped[date_str] += t.amount

        sorted_points = sorted(grouped.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))
        return [(d, round(v, 2)) for d, v in sorted_points]