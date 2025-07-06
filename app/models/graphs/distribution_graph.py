import numpy as np
from kivy.utils import get_color_from_hex
from app.utils.helpers import set_bins
from kivy.properties import ListProperty
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib.pyplot as plt
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.theme import ACCENT_COLOR
from app.utils.language_mapper import LanguageMapper as LM

class DistributionGraph(BaseGraphWidget):
    """
    Histogram of transaction amounts with green background and orange bars/labels.
    """
    transactions = ListProperty([])

    def fit(self, transactions):
        amounts = [abs(tx.amount) for tx in transactions]
        if not amounts:
            return [], []
        counts, bins = np.histogram(amounts, bins=set_bins(len(transactions)))
        centers = [(bins[i] + bins[i+1]) / 2 for i in range(len(counts))]
        return centers, counts

    def _render(self):
        self.clear_widgets()
        xs, ys = self.fit(self.transactions)
        if not xs or len(xs) < 2:
            print("[DistributionGraph] Недостатньо даних для побудови графіка")
            return

        fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.15)

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

        ax.tick_params(colors="#FFFFFF", rotation=90, labelsize=8, axis='y')
        ax.tick_params(colors="#FFFFFF", labelsize=8, axis='x')
        ax.set_xlabel(LM.stat_name("total"), color="#AAAAAA", fontsize=8)
        ax.set_ylabel(LM.stat_name("count"), color="#AAAAAA", fontsize=8)

        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (1, 1)
        canvas.pos_hint = {}
        self.add_widget(canvas)


# from app.utils.helpers import set_bins
# from app.models.graphs.base_graph import BaseGraphWidget
# import numpy as np

# class DistributionGraph(BaseGraphWidget):
#     """
#     Prepares histogram data of transaction amounts.
#     """
#     def fit(self, transactions):
#         amounts = [abs(tx.amount) for tx in transactions]
#         if not amounts:
#             return {"x": [], "y": []}
#         counts, bins = np.histogram(amounts, bins=set_bins(len(transactions)))
#         centers = [(bins[i] + bins[i + 1]) / 2 for i in range(len(counts))]
#         return {"x": centers, "y": counts}