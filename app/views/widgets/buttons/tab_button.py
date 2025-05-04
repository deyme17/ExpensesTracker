from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty
from kivy.graphics import Color, Line
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from app.utils.theme import (
    get_text_primary_color,
    ACCENT_COLOR,
)


class TabButton(BoxLayout):
    """
    A button for a tab interface.
    """
    text = StringProperty('')
    icon = StringProperty('')
    is_selected = BooleanProperty(False)
    badge_count = StringProperty('')
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint_x', None)
        kwargs.setdefault('width', dp(80))
        kwargs.setdefault('padding', dp(5))
        
        super(TabButton, self).__init__(**kwargs)
        
        # icon label
        self.icon_label = Label(
            text=self.icon,
            font_size=sp(24),
            color=get_text_primary_color(),
            size_hint_y=0.6
        )
        
        # text label
        self.text_label = Label(
            text=self.text,
            font_size=sp(12),
            color=get_text_primary_color(),
            size_hint_y=0.4
        )
        
        self.add_widget(self.icon_label)
        self.add_widget(self.text_label)
        
        # bind properties
        self.bind(text=self._update_text)
        self.bind(icon=self._update_icon)
        self.bind(is_selected=self._update_canvas)
        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self.bind(badge_count=self._update_badge)
        
        Clock.schedule_once(lambda dt: self._update_canvas(), 0)
    
    def _update_canvas(self, *args):
        """Update the button's canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_selected:
                Color(*get_color_from_hex(ACCENT_COLOR))
                Line(
                    points=[
                        self.x + dp(10), self.y,
                        self.x + self.width - dp(10), self.y
                    ],
                    width=dp(2)
                )
    
    def _update_text(self, instance, value):
        """Update text label when text property changes."""
        self.text_label.text = value
    
    def _update_icon(self, instance, value):
        """Update icon label when icon property changes."""
        self.icon_label.text = value
    
    def _update_badge(self, instance, value):
        """Update badge when badge_count property changes."""
        pass
    
    def on_touch_down(self, touch):
        """Handle touch events."""
        if self.collide_point(*touch.pos):
            self.is_selected = True
            return True
        return super(TabButton, self).on_touch_down(touch)