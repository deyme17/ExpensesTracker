import numpy as np
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty

from kivy.logger import Logger
Logger.setLevel("ERROR")
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib.pyplot as plt
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.theme import ACCENT_COLOR

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

        dark_bg = get_color_from_hex("#08382C")
        fig.patch.set_facecolor("#0A4035")
        ax.set_facecolor(dark_bg)

        ax.grid(True, color=(1, 1, 1, 0.005), linestyle='-', linewidth=0.1)

        # hist
        ax.bar(
            xs, ys,
            color=get_color_from_hex(ACCENT_COLOR),
            edgecolor="#042721",
            width=(xs[1] - xs[0])
        )

        ax.tick_params(colors="#FFFFFF", rotation=45, labelsize=5)

        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (1, 1)
        canvas.pos_hint = {"top": 1}
        self.add_widget(canvas)
