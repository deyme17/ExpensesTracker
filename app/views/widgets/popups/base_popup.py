from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.graphics import Color
from app.views.widgets.buttons.styled_button import StyledButton
from kivy.metrics import dp, sp


from app.utils.theme import (
    get_background_color, get_text_primary_color, get_color_from_hex,
    FONT_SIZE_MEDIUM
)

class BasePopup(Popup):
    """Base class for custom popups."""
    message = StringProperty("")
    
    def __init__(self, message, **kwargs):
        super(BasePopup, self).__init__(**kwargs)
        self.message = message
        self.title = ""
        self.size_hint = (0.8, 0.3)
        self.background = ""
        self.background_color = (0, 0, 0, 0)
        self.auto_dismiss = True
        
        content = self._create_content()
        self.content = content
        
        Clock.schedule_once(lambda dt: self.dismiss(), 2)
    
    def _create_content(self):
        """Create the content of the popup. Override in subclasses."""
        content = BoxLayout(orientation="vertical", padding=dp(10))
        
        label = Label(
            text=self.message,
            color=get_text_primary_color(),
            font_size=sp(FONT_SIZE_MEDIUM),
            halign="center",
            valign="middle"
        )
        label.bind(size=label.setter("text_size"))
        
        content.add_widget(label)
        return content
    
    def on_open(self):
        """Called when the popup is opened."""
        super(BasePopup, self).on_open()
        
        with self.canvas.before:
            self._bg_color = Color(rgba=self._get_background_color())
            self._bg_rect = StyledButton(
                pos=self.pos, size=self.size, radius=[dp(10)],
                bg_color=get_color_from_hex('#0A4035')
            )


        self.bind(pos=self._update_canvas, size=self._update_canvas)
    
    def _update_canvas(self, instance, value):
        """Update the canvas when size or position changes."""
        if hasattr(self, '_bg_rect'):
            self._bg_rect.pos = instance.pos
            self._bg_rect.size = instance.size
    
    def _get_background_color(self):
        """Get the background color for the popup. Override in subclasses."""
        return get_background_color()