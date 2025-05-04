from kivy.uix.widget import Widget
from kivy.clock import Clock

class BaseGraphWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        Clock.schedule_once(lambda dt: self._build())

    def on_size(self, *args):
        self._build()

    def on_pos(self, *args):
        self._build()

    def _build(self):
        pass