from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from app.services.analytics.graph_factory import GraphFactory
import hashlib

class GraphSection(BoxLayout):
    chart_type = StringProperty()
    controller = ObjectProperty()
    transaction_type = StringProperty()
    transactions = ObjectProperty()
    category = StringProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(10)
        self.graph_widget = None
        self._last_graph_key = None
        Clock.schedule_once(lambda dt: self._load_graph())

    def _load_graph(self):
        current_key = self._compute_graph_key()

        if current_key == self._last_graph_key and self.graph_widget:
            return

        if self.graph_widget:
            self.remove_widget(self.graph_widget)

        try:
            self.graph_widget = GraphFactory.create_graph(
                chart_type=self.chart_type,
                controller=self.controller,
                transaction_type=self.transaction_type,
                transactions=self.transactions,
                category=self.category
            )
            self.graph_widget.opacity = 0
            self.add_widget(self.graph_widget)
            Animation(opacity=1, d=0.5).start(self.graph_widget)
            self._last_graph_key = current_key
        except Exception as e:
            print(f"[GraphSection] Помилка створення графіка: {e}")
            self.graph_widget = None

    def update_graph(self, transactions=None, chart_type=None):
        if chart_type is not None:
            self.chart_type = str(chart_type)
        if transactions is not None:
            self.transactions = transactions
        self._load_graph()

    def _compute_graph_key(self):
        if not self.transactions:
            return None
        hasher = hashlib.md5()
        for tx in self.transactions:
            hasher.update(f"{tx.transaction_id}-{tx.amount}-{tx.date}".encode())
        key = f"{self.chart_type}-{self.transaction_type}-{self.category or 'all'}"
        hasher.update(key.encode())
        return hasher.hexdigest()