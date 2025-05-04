from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from app.utils.theme import get_text_primary_color
from kivy.clock import Clock

from app.utils.theme import (
    PRIMARY_COLOR,
    FONT_SIZE_MEDIUM
)

class StyledButton(Button):
    """Custom styled button with rounded corners and background color."""
    
    def __init__(self, bg_color, **kwargs):
        super(StyledButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.color = get_text_primary_color()
        self.bold = True
        
        self.bind(size=self.update_background, pos=self.update_background)
        
        Clock.schedule_once(lambda dt: self.update_background(), 0)
    
    def update_background(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex(self.bg_color))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

            
class RoundedButton(Button):
    """
    A button with rounded corners and customizable colors.
    """
    bg_color = StringProperty(PRIMARY_COLOR)
    bg_color_down = StringProperty('')
    border_radius = ListProperty([dp(10)])
    text_color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', (0, 0, 0, 0))
        kwargs.setdefault('color', kwargs.get('text_color', [1, 1, 1, 1]))
        kwargs.setdefault('halign', 'center')
        kwargs.setdefault('valign', 'middle')
        kwargs.setdefault('font_size', sp(FONT_SIZE_MEDIUM))
        
        super(RoundedButton, self).__init__(**kwargs)
        
        if not self.bg_color_down:
            color = get_color_from_hex(self.bg_color)
            if not self.bg_color_down:
                if self.bg_color.startswith('#'):
                    self.bg_color_down = '#0A352D'
                else:
                    self.bg_color_down = self.bg_color
            
        # bind properties
        self.bind(pos=self._update_canvas)
        self.bind(size=self._update_canvas)
        self.bind(state=self._update_canvas)
        
        Clock.schedule_once(lambda dt: self._update_canvas(), 0)
    
    def _update_canvas(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            if self.state == 'down':
                Color(*get_color_from_hex(self.bg_color_down))
            else:
                Color(*get_color_from_hex(self.bg_color))
            
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.border_radius
            )