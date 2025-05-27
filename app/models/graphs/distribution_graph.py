import numpy as np
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty
try:
    from gar_mat.backend_kivyagg import FigureCanvasKivyAgg
except ImportError:
    raise ImportError("kivy_garden.matplotlib not found. Install via: garden install matplotlib")
import matplotlib.pyplot as plt
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.constants import ACCENT_COLOR

class DistributionGraph(BaseGraphWidget):
    """
    Histogram of transaction amounts with green background and orange bars/labels.
    """
    transactions = ListProperty([])

    def fit(self, transactions):
        amounts = [abs(tx.amount) for tx in transactions]
        if not amounts:
            return [], []
        counts, bins = np.histogram(amounts, bins=10)
        centers = [(bins[i] + bins[i+1]) / 2 for i in range(len(counts))]
        return centers, counts

    def _render(self):
        self.clear_widgets()
        xs, ys = self.fit(self.transactions)
        if not xs:
            return




        fig = plt.figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.1)


        for spine in ax.spines.values():
            spine.set_visible(False)

        # фон — темніший
        dark_bg = get_color_from_hex("#08382C")  # півтону темніше
        fig.patch.set_facecolor("#0A4035")
        ax.set_facecolor(dark_bg)


         # сітка
        ax.grid(True, color=(1, 1, 1, 0.005), linestyle='-', linewidth=0.1)

        # гістограма
        ax.bar(
            xs, ys,
            color=get_color_from_hex(ACCENT_COLOR),
            edgecolor="#042721",
            width=(xs[1] - xs[0])
        )

        # підписи осі X
        ax.tick_params(colors="#FFFFFF", rotation=45, labelsize=5)

       

        # інтерактивне полотно
        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (1, 1)
        canvas.pos_hint = {"top": 1}
        self.add_widget(canvas)