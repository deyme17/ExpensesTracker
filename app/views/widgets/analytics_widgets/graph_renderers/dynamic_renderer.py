from app.views.widgets.analytics_widgets.graph_renderers.base_renderer import Renderer
from kivy.utils import get_color_from_hex
from matplotlib.dates import DateFormatter
from app.utils.language_mapper import LanguageMapper as LM


class DynamicRenderer(Renderer):
    def _render(self, dates, values):
        if not dates:
            return

        fig, ax = self._setup_figure()
        
        # line
        ax.grid(True, color=(1, 1, 1, 0.005), linestyle='-', linewidth=0.1)
        ax.plot(
            dates,
            values,
            marker='o',
            linestyle='-',
            color=get_color_from_hex(self.ACCENT_COLOR),
            markersize=3,
            linewidth=1.5
        )

        # ticks setting
        ax.xaxis.set_major_formatter(DateFormatter('%d.%m'))
        ax.tick_params(colors="#FFFFFF", rotation=90, labelsize=8, axis='y')
        ax.tick_params(colors="#FFFFFF", labelsize=8, axis='x')
        ax.set_xlabel(LM.field_name("date"), color="#AAAAAA", fontsize=8)
        ax.set_ylabel(LM.stat_name("total"), color="#AAAAAA", fontsize=8)
        fig.autofmt_xdate()

        self._add_canvas(fig)