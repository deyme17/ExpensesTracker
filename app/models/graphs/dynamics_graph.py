from datetime import datetime
from kivy.utils import get_color_from_hex
try:
        from resources.gar_mat.backend_kivyagg import FigureCanvasKivyAgg
except ImportError:
    raise ImportError("kivy_garden.matplotlib not found. Install via: garden install matplotlib")
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.constants import ACCENT_COLOR

class DynamicsGraph(BaseGraphWidget):
    """
    Line graph of transaction sums over time with green background and orange line/labels.
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
        

        fig = plt.figure(figsize=(2, 2), dpi=75)
        ax = fig.add_subplot(111)

        for spine in ax.spines.values():
            spine.set_visible(False)

        # фон — темніший
        dark_bg = get_color_from_hex("#08382C")  # півтону темніше
        fig.patch.set_facecolor("#0A4035")
        ax.set_facecolor(dark_bg)


         # сітка
        ax.grid(True, color=(1, 1, 1, 0.005), linestyle='-', linewidth=0.1)

        # orange line
        ax.plot(dates, values, marker='o', linestyle='-', color=get_color_from_hex(ACCENT_COLOR), markersize = 1)
        # orange labels
        ax.xaxis.set_major_formatter(DateFormatter('%d.%m'))
        ax.tick_params(colors="#FFFFFF")
        fig.autofmt_xdate()
        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (1, 1)
        self.add_widget(canvas)
