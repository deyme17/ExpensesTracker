from kivy.graphics import Color, Ellipse
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.theme import get_category_color

class ShareGraph(BaseGraphWidget):
    def __init__(self, controller, transaction_type, period, **kwargs):
        self.controller = controller
        self.transaction_type = transaction_type
        self.period = period
        super().__init__(**kwargs)

    def _build(self):
        self.data = self.controller.get_category_share_data(self.transaction_type, self.period)
        self.canvas.clear()
        if not self.data:
            return

        total = sum(amount for _, amount, _ in self.data)
        if total == 0:
            return

        angle_start = 0
        size = min(self.width, self.height) * 0.9
        center_x = self.center_x - size / 2
        center_y = self.center_y - size / 2

        with self.canvas:
            for i, (category, amount, _) in enumerate(self.data):
                angle_end = angle_start + 360 * (amount / total)
                Color(*get_category_color(category))
                Ellipse(pos=(center_x, center_y), size=(size, size), angle_start=angle_start, angle_end=angle_end)
                angle_start = angle_end