from app.models.graphs.base_graph import BaseGraph


class DynamicsGraph(BaseGraph):
    """
    Line graph model of transaction sums over time.
    """
    def fit(self, transactions):
        data = {}

        for tx in transactions:
            date = tx.date if hasattr(tx.date, 'to_pydatetime') else tx.date
            date = date.to_pydatetime() if hasattr(date, 'to_pydatetime') else date
            data.setdefault(date, 0)
            data[date] += tx.amount

        dates, values = zip(*sorted(data.items())) if data else ([], [])
        return dates, values