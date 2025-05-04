from kivy.graphics import Color, Rectangle
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.theme import get_primary_color

class DistributionGraph(BaseGraphWidget):
    def __init__(self, controller, transaction_type, period, category, **kwargs):
        self.controller = controller
        self.transaction_type = transaction_type
        self.period = period
        self.category = category
        super().__init__(**kwargs)

    def _build(self):
        self.data = self.controller.get_distribution_data(
            self.transaction_type, self.period, self.category
        )
        self.canvas.clear()
        if not self.data:
            return

        num_bars = len(self.data)
        max_count = max((count for _, count in self.data), default=0)
        if max_count == 0:
            return

        spacing = 10
        bar_width = (self.width - (num_bars + 1) * spacing) / max(num_bars, 1)
        chart_height = self.height * 0.9
        base_y = self.y + self.height * 0.05

        with self.canvas:
            Color(*get_primary_color())
            for i, (_, count) in enumerate(self.data):
                bar_height = (count / max_count) * chart_height
                x = self.x + spacing + i * (bar_width + spacing)
                Rectangle(pos=(x, base_y), size=(bar_width, bar_height))
