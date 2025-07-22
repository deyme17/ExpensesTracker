from app.views.widgets.analytics_widgets.graph_renderers.base_renderer import Renderer
from kivy.utils import get_color_from_hex
from app.utils.language_mapper import LanguageMapper as LM


class DistributionRenderer(Renderer):
    graph_key = "distribution"
    
    def _render(self, xs, ys):
        if not xs or len(xs) < 2:
            print("[DistributionGraph] Not enough data for distribution plotting.")
            return

        fig, ax = self._setup_figure()
        
        # hist
        ax.grid(True, color=(1, 1, 1, 0.005), linestyle='-', linewidth=0.1)
        ax.bar(
            xs, ys,
            color=get_color_from_hex(self.ACCENT_COLOR),
            edgecolor="#042721",
            width=(xs[1] - xs[0]) if len(xs) > 1 else 1
        )

        # ticks settings
        ax.tick_params(colors="#FFFFFF", rotation=90, labelsize=8, axis='y')
        ax.tick_params(colors="#FFFFFF", labelsize=8, axis='x')
        ax.set_xlabel(LM.stat_name("total"), color="#AAAAAA", fontsize=8)
        ax.set_ylabel(LM.stat_name("count"), color="#AAAAAA", fontsize=8)

        self._add_canvas(fig)