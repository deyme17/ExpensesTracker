from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from app.utils.constants import CHART_TYPE_HISTOGRAM, CHART_TYPE_LINE, CHART_TYPE_PIE
from kivy.app import App

class GraphSection(BoxLayout):
    """
    Displays graphs based on chart_type and transactions, delegating graph creation to AnalyticsController.
    """
    chart_type = StringProperty(CHART_TYPE_LINE)

    def update_graph(self, transactions, chart_type=None):
        self.clear_widgets()
        if chart_type:
            self.chart_type = chart_type

        app = App.get_running_app()
        controller = app.analytics_controller
        transaction_type = app.analytics_screen.current_type if hasattr(app, "analytics_screen") else None

        widget = controller.create_graph(
            chart_type=self.chart_type,
            transactions=transactions,
            transaction_type=transaction_type
        )

        if widget:
            widget._render()
            widget.size_hint = (1, 1)
            self.add_widget(widget)
