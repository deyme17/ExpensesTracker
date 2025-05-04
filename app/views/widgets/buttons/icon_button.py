from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from app.utils.theme import (
    get_text_primary_color,
    PRIMARY_COLOR, ACCENT_COLOR
)


class IconButton(BoxLayout):
    """
    A button with an icon and optional text.
    """
    text = StringProperty('')
    icon = StringProperty('')
    bg_color = StringProperty(PRIMARY_COLOR)
    is_selected = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(60), dp(60)))
        kwargs.setdefault('spacing', dp(5))
        
        super(IconButton, self).__init__(**kwargs)
        
        # bind properties
        self.bind(pos=self._update_canvas)
        self.bind(size=self._update_canvas)
        self.bind(is_selected=self._update_canvas)
        self.bind(text=self._update_text)
        self.bind(icon=self._update_icon)
        
        # icon widget
        self.icon_widget = Label(
            text=self.icon,
            font_size=sp(24),
            color=get_text_primary_color(),
            size_hint=(1, 0.7)
        )
        
        # text label
        self.text_label = Label(
            text=self.text,
            font_size=sp(12),
            color=get_text_primary_color(),
            size_hint=(1, 0.3)
        )
        
        self.add_widget(self.icon_widget)
        self.add_widget(self.text_label)
        
        Clock.schedule_once(lambda dt: self._update_canvas(), 0)
    
    def _update_canvas(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_selected:
                Color(*get_color_from_hex(ACCENT_COLOR))
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(10)]
                )
            else:
                Color(*get_color_from_hex(self.bg_color))
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(10)]
                )
    
    def _update_text(self, instance, value):
        """Update text label when text property changes."""
        self.text_label.text = value
    
    def _update_icon(self, instance, value):
        """Update icon when icon property changes."""
        self.icon_widget.text = value
    
    def on_touch_down(self, touch):
        """Handle touch events."""
        if self.collide_point(*touch.pos):
            self.is_selected = True
            return True
        return super(IconButton, self).on_touch_down(touch)