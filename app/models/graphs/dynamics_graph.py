from datetime import datetime
from kivy.utils import get_color_from_hex
from kivy.logger import Logger
Logger.setLevel("ERROR")
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.theme import ACCENT_COLOR
from app.utils.language_mapper import LanguageMapper as LM

class DynamicsGraph(BaseGraphWidget):
    """
    Line graph of transaction sums over time with improved styling.
    """
    def fit(self, transactions):
        data = {}
        for tx in transactions:
            date = tx.date if hasattr(tx.date, 'to_pydatetime') else tx.date
            date = date.to_pydatetime() if hasattr(date, 'to_pydatetime') else date
            data.setdefault(date, 0)
            data[date] += tx.amount
        dates, values = zip(*sorted(data.items())) if data else ([], [])
        return dates, values

    def _render(self):
        self.clear_widgets()
        dates, values = self.fit(self.transactions)
        if not dates:
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

        ax.plot(
            dates,
            values,
            marker='o',
            linestyle='-',
            color=get_color_from_hex(ACCENT_COLOR),
            markersize=3,
            linewidth=1.5
        )

        ax.xaxis.set_major_formatter(DateFormatter('%d.%m'))
        ax.tick_params(colors="#FFFFFF", rotation=90, labelsize=8, axis='y')
        ax.tick_params(colors="#FFFFFF", labelsize=8, axis='x')
        ax.set_xlabel(LM.field_name("date"), color="#AAAAAA", fontsize=8)
        ax.set_ylabel(LM.stat_name("total"), color="#AAAAAA", fontsize=8)

        fig.autofmt_xdate()

        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (1, 1)
        canvas.pos_hint = {}
        self.add_widget(canvas)


# from app.models.graphs.base_graph import BaseGraphWidget

# class DynamicsGraph(BaseGraphWidget):
#     """
#     Prepares line graph data of transaction sums over time.
#     """
#     def fit(self, transactions):
#         data = {}
#         for tx in transactions:
#             date = tx.date if hasattr(tx.date, 'to_pydatetime') else tx.date
#             date = date.to_pydatetime() if hasattr(date, 'to_pydatetime') else date
#             data.setdefault(date, 0)
#             data[date] += tx.amount
#         if not data:
#             return {"x": [], "y": []}
#         dates, values = zip(*sorted(data.items()))
#         return {"x": dates, "y": values}