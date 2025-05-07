from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from app.services.graph_factory import GraphFactory


class GraphSection(BoxLayout):
    """
    The widget responsible for displaying the graph depending on the type.
    """
    chart_type = StringProperty()
    controller = ObjectProperty()
    transaction_type = StringProperty()
    period = ObjectProperty()
    category = StringProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(10)
        self.graph_widget = None
        Clock.schedule_once(lambda dt: self._load_graph())

    def _load_graph(self):
        if self.graph_widget:
            self.remove_widget(self.graph_widget)

        try:
            self.graph_widget = GraphFactory.create_graph(
                chart_type=self.chart_type,
                controller=self.controller,
                transaction_type=self.transaction_type,
                period=self.period,
                category=self.category
            )
            self.graph_widget.opacity = 0
            self.add_widget(self.graph_widget)
            Animation(opacity=1, d=0.5).start(self.graph_widget)
        except Exception as e:
            print(f"[GraphSection] Помилка створення графіка: {e}")
            self.graph_widget = None

    def update_graph(self, chart_type=None):
        """
        Updates the schedule. If a new type is transmitted, it changes it.
        """
        if chart_type:
            self.chart_type = chart_type
        self._load_graph()
