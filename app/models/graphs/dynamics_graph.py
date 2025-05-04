from kivy.graphics import Color, Line, Ellipse
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.theme import get_secondary_color


class DynamicsGraph(BaseGraphWidget):
    def __init__(self, controller, transaction_type, period, category, **kwargs):
        self.controller = controller
        self.transaction_type = transaction_type
        self.period = period
        self.category = category
        super().__init__(**kwargs)

    def _build(self):
        self.data = self.controller.get_dynamics_data(
            self.transaction_type, self.period, self.category
        )
        self.canvas.clear()
        if not self.data or len(self.data) < 2:
            return

        max_amount = max((amount for _, amount in self.data), default=0)
        if max_amount == 0:
            return

        step_x = self.width / (len(self.data) - 1)
        max_height = self.height * 0.9
        base_y = self.y + self.height * 0.05

        coords = []
        for i, (_, amount) in enumerate(self.data):
            x = self.x + i * step_x
            y = base_y + (amount / max_amount) * max_height
            coords.extend([x, y])

        with self.canvas:
            Color(*get_secondary_color())
            Line(points=coords, width=2)
            for i in range(0, len(coords), 2):
                Ellipse(pos=(coords[i] - 3, coords[i+1] - 3), size=(6, 6))