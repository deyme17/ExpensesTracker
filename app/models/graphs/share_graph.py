from collections import defaultdict
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty

from kivy.logger import Logger
Logger.setLevel("ERROR")
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib.pyplot as plt
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.theme import ACCENT_COLOR
from app.services.crud_services.static_data import StaticDataService
from app.utils.language_mapper import LanguageMapper


_static_service = StaticDataService()
_static_service.get_categories()

class ShareGraph(BaseGraphWidget):
    """
    Pie chart of transaction share by category with green background and orange texts.
    Uses singleton StaticDataService to avoid repeated DB calls.
    """
    transactions = ListProperty([])

    def fit(self, transactions):
        totals = defaultdict(float)
        for tx in transactions:
            raw_name = _static_service.get_category_name_by_mcc(tx.mcc_code)
            translated_name = LanguageMapper.category(raw_name)
            totals[translated_name] += abs(tx.amount)

        items = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:10]

        if not items:
            return [], []
        labels, values = zip(*items)
        return labels, values

    def _render(self):
        self.clear_widgets()
        labels, values = self.fit(self.transactions)
        if not labels:
            return

        fig = plt.figure(figsize=(5, 3), dpi=200)
        ax = fig.add_subplot(111)

        for spine in ax.spines.values():
            spine.set_visible(False)

        dark_bg = get_color_from_hex("#08382C")
        fig.patch.set_facecolor("#0A4035")
        ax.set_facecolor(dark_bg)

        wedges, _ = ax.pie(
            values,
            labels=None,
            startangle=90,
            radius=1.3,
            wedgeprops={"linewidth": 0.5, "edgecolor": "#0A4035"}
        )
        ax.set_position([0.25, 0.3, 0.5, 0.7])    

        legend_labels = [
        f"{label[:10]} — {int(value)}₴" for label, value in zip(labels, values)
    ]
        ax.legend(
                wedges,
                legend_labels,
                loc='upper center',
                bbox_to_anchor=(0.5, -0.1),
                ncol=2,
                fontsize=4,
                labelcolor=get_color_from_hex(ACCENT_COLOR),
                facecolor=get_color_from_hex('#0A4035'),
                edgecolor="none",
                handlelength=0.8,
                columnspacing=0.5
            )
        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (1, 1)
        canvas.pos_hint = {"center_x": 0.5, "top": 1}
        self.add_widget(canvas)
