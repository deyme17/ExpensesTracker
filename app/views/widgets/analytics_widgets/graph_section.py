from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from app.utils.constants import (
    CHART_TYPE_HISTOGRAM,
    CHART_TYPE_LINE,
    CHART_TYPE_PIE
)
from app.views.widgets.analytics_widgets.graph_renderers.dist_renderer import DistributionRenderer
from app.views.widgets.analytics_widgets.graph_renderers.dynamic_renderer import DynamicRenderer
from app.views.widgets.analytics_widgets.graph_renderers.share_renderer import ShareRenderer


class GraphSection(BoxLayout):
    """
    Container for displaying financial analytics graphs.
    Properties:
        chart_type: Current visualization type (histogram/line/pie)
    Args:
        graph_factory: Factory for creating graph visualizations
    """
    chart_type = StringProperty(CHART_TYPE_LINE)

    def __init__(self, graph_factory, **kwargs):
        super().__init__(**kwargs)
        self._factory = graph_factory

        self._renderer_map = {
            CHART_TYPE_HISTOGRAM: DistributionRenderer,
            CHART_TYPE_LINE: DynamicRenderer,
            CHART_TYPE_PIE: ShareRenderer
        }

    def update_graph(self, transactions, chart_type=None):
        """
        Updates the displayed graph with new data.
        Args:
            transactions: Transaction data to visualize
            chart_type: Chart type to switch to
        """
        self.clear_widgets()
        if chart_type:
            self.chart_type = chart_type

        RendererCls = self._renderer_map.get(self.chart_type)
        if not RendererCls:
            return

        renderer = RendererCls()
        widget = self._factory.create_graph(renderer, transactions)
        widget.size_hint = (1, 1)
        self.add_widget(widget)