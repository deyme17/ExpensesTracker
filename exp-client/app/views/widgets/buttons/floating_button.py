from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.graphics import Color,Ellipse
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from app.utils.theme import (
    get_text_primary_color,
    ACCENT_COLOR,
)

class FloatingActionButton(Button):
    """
    A circular floating action button.
    """
    bg_color = StringProperty(ACCENT_COLOR)
    icon = StringProperty("+")
    
    def __init__(self, **kwargs):
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("size", (dp(56), dp(56)))
        kwargs.setdefault("text", self.icon)
        kwargs.setdefault("font_size", sp(30))
        kwargs.setdefault("bold", True)
        kwargs.setdefault("color", get_text_primary_color())
        
        super(FloatingActionButton, self).__init__(**kwargs)
        
        # bind properties
        self.bind(pos=self._update_canvas)
        self.bind(size=self._update_canvas)
        self.bind(state=self._update_canvas)
        
        Clock.schedule_once(lambda dt: self._update_canvas(), 0)
    
    def _update_canvas(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.2)
            Ellipse(pos=(self.x + dp(2), self.y - dp(2)), size=self.size)
            
            if self.state == "down":
                r, g, b = get_color_from_hex(self.bg_color)[:3]
                Color(r*0.8, g*0.8, b*0.8, 1)
            else:
                Color(*get_color_from_hex(self.bg_color))
            
            Ellipse(pos=self.pos, size=self.size)