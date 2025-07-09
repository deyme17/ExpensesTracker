from collections import defaultdict
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.theme import ACCENT_COLOR
from app.utils.constants import SHARE_NUM
from app.utils.language_mapper import LanguageMapper

class ShareGraph(BaseGraphWidget):
    """
    Pie chart of transaction share by category with styled layout.
    """
    transactions = ListProperty([])

    def fit(self, transactions):
        totals = defaultdict(float)

        from app.services.crud_services.category import CategoryService
        _category_service = CategoryService()
        _category_service.get_categories()
        
        for tx in transactions:
            raw_name = _category_service.get_category_name_by_mcc(tx.mcc_code)
            translated_name = LanguageMapper.category(raw_name)
            totals[translated_name] += abs(tx.amount)

        items = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:SHARE_NUM]

        if not items:
            return [], []
        labels, values = zip(*items)
        return labels, values

    def _render(self):
        self.clear_widgets()
        labels, values = self.fit(self.transactions)
        if not labels:
            return

        fig = plt.figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.3)

        for spine in ax.spines.values():
            spine.set_visible(False)

        dark_bg = get_color_from_hex("#08382C")
        fig.patch.set_facecolor("#0A4035")
        ax.set_facecolor(dark_bg)

        wedges, _ = ax.pie(
            values,
            labels=None,
            startangle=90,
            radius=1.5,
            wedgeprops={"linewidth": 0.5, "edgecolor": "#0A4035"}
        )
        ax.set_position([0.2, 0.3, 0.6, 0.6])

        legend_labels = [
            f"{label[:16]} — {int(value)}" for label, value in zip(labels, values)
        ]
        ax.legend(
            wedges,
            legend_labels,
            loc='upper center',
            bbox_to_anchor=(0.5, -0.25),
            ncol=3,
            fontsize=6,
            labelcolor=get_color_from_hex(ACCENT_COLOR),
            facecolor=get_color_from_hex('#0A4035'),
            edgecolor="none",
            handlelength=0.8,
            columnspacing=0.5,
            frameon=False
        )

        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (1, 1)
        canvas.pos_hint = {}
        self.add_widget(canvas)

# from collections import defaultdict
# from datetime import datetime
# import numpy as np

# from app.models.graphs.base_graph import BaseGraphWidget
# from app.utils.helpers import set_bins
# from app.services.crud_services.static_data import StaticDataService
# from app.utils.language_mapper import LanguageMapper as LM
# from app.utils.constants import SHARE_NUM

# _category_service = StaticDataService()
# _category_service.get_categories()  # preload cache

# class ShareGraph(BaseGraphWidget):
#     """
#     Prepares pie chart data of transaction share by category.
#     """
#     def fit(self, transactions):
#         totals = defaultdict(float)
#         for tx in transactions:
#             raw_name = _category_service.get_category_name_by_mcc(tx.mcc_code)
#             translated_name = LM.category(raw_name)
#             totals[translated_name] += abs(tx.amount)

#         items = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:SHARE_NUM]

#         if not items:
#             return {"labels": [], "values": []}
#         labels, values = zip(*items)
#         return {"labels": labels, "values": values}
