from abc import abstractmethod
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


class Renderer(BoxLayout):
    BACKGROUND_COLOR = "#0A4035"
    DARK_BG = "#08382C"

    @abstractmethod
    def _render(self, *args, **kwargs):
        pass

    def _setup_figure(self, figsize=(5, 4), dpi=100):
        self.clear_widgets()
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_subplot(111)
        
        fig.patch.set_facecolor(self.BACKGROUND_COLOR)
        ax.set_facecolor(self.DARK_BG)
        
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        return fig, ax

    def _add_canvas(self, fig):
        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (1, 1)
        canvas.pos_hint = {}
        self.add_widget(canvas)