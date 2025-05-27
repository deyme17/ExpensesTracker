from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from app.models.graphs.distribution_graph import DistributionGraph
from app.models.graphs.dynamics_graph import DynamicsGraph
from app.models.graphs.share_graph import ShareGraph
from app.utils.constants import CHART_TYPE_HISTOGRAM, CHART_TYPE_LINE, CHART_TYPE_PIE

class GraphSection(BoxLayout):
    """
    Displays graphs based on chart_type and transactions, filling full area and updating on filter.
    """
    chart_type = StringProperty(CHART_TYPE_LINE)

    def update_graph(self, transactions, chart_type=None):
        self.clear_widgets()
        if chart_type:
            self.chart_type = chart_type
        if self.chart_type == CHART_TYPE_HISTOGRAM:
            widget = DistributionGraph()
        elif self.chart_type == CHART_TYPE_LINE:
            widget = DynamicsGraph()
        elif self.chart_type == CHART_TYPE_PIE:
            widget = ShareGraph()
        else:
            return
        # apply filtered transactions and render
        widget.transactions = transactions
        widget._render()
        widget.size_hint = (1, 1)
        self.add_widget(widget)
