from app.utils.constants import (
    CHART_TYPE_HISTOGRAM, CHART_TYPE_PIE, CHART_TYPE_LINE
)

from app.models.graphs.distribution_graph import DistributionGraph
from app.models.graphs.share_graph import ShareGraph
from app.models.graphs.dynamics_graph import DynamicsGraph


class GraphFactory:
    chart = {
        CHART_TYPE_HISTOGRAM: DistributionGraph,
        CHART_TYPE_PIE: ShareGraph,
        CHART_TYPE_LINE: DynamicsGraph,
    }

    @classmethod
    def create_graph(cls, chart_type, controller, transaction_type, period, category=None):
        graph_class = cls.chart.get(chart_type)
        if not graph_class:
            raise ValueError(f"Невідомий тип графіка: {chart_type}")

        return graph_class(
            controller=controller,
            transaction_type=transaction_type,
            period=period,
            category=category
        )