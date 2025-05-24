from app.utils.constants import (
    CHART_TYPE_HISTOGRAM, CHART_TYPE_PIE, CHART_TYPE_LINE
)
from utils.language_mapper import LanguageMapper as LM
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
    def create_graph(cls, chart_type, controller, transaction_type, transactions, category=None):
        graph_class = cls.chart.get(chart_type)
        if not graph_class:
            raise ValueError(LM.message("unknown_chart_type").format(type=chart_type))

        widget = graph_class()
        widget.controller = controller
        widget.transaction_type = transaction_type
        widget.transactions = transactions
        widget.category = category
        return widget
