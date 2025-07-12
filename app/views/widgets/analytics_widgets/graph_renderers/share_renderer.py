from app.views.widgets.analytics_widgets.graph_renderers.base_renderer import Renderer
from app.utils.theme import ACCENT_COLOR
from kivy.utils import get_color_from_hex


class ShareRenderer(Renderer):
    def _render(self, labels, values):
        if not labels or len(labels) != len(values):
            return

        fig, ax = self._setup_figure(figsize=(6, 4))
        
        # share
        wedges, _ = ax.pie(
            values,
            labels=None,
            startangle=90,
            radius=1.5,
            wedgeprops={"linewidth": 0.5, "edgecolor": self.BACKGROUND_COLOR}
        )
        ax.set_position([0.2, 0.3, 0.6, 0.6])

        # legend
        legend_labels = [f"{label[:16]} — {int(value)}" for label, value in zip(labels, values)]
        ax.legend(
            wedges,
            legend_labels,
            loc='upper center',
            bbox_to_anchor=(0.5, -0.25),
            ncol=3,
            fontsize=6,
            labelcolor=get_color_from_hex(ACCENT_COLOR),
            facecolor=get_color_from_hex(self.BACKGROUND_COLOR),
            edgecolor="none",
            handlelength=0.8,
            columnspacing=0.5,
            frameon=False
        )

        self._add_canvas(fig)