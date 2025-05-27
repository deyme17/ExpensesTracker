from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import StringProperty
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from app.utils.theme import (
    get_text_primary_color, get_secondary_color,
    FONT_SIZE_MEDIUM
)


class StyledTextInput(TextInput):
    """
    A styled text input with dark visible text and proper padding.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault("background_color", (0, 0, 0, 0)) 
        kwargs.setdefault("foreground_color", get_color_from_hex('#212121')) 
        kwargs.setdefault("cursor_color", get_color_from_hex('#212121'))  
        kwargs.setdefault("hint_text_color", get_color_from_hex('#B0BEC5'))  
        kwargs.setdefault("font_size", sp(16))
        kwargs.setdefault("multiline", False)
        kwargs.setdefault("padding", [dp(15), dp(12), dp(15), dp(12)])
        kwargs.setdefault("write_tab", False)
        
        super(StyledTextInput, self).__init__(**kwargs)
        
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        Clock.schedule_once(lambda dt: self.update_canvas(), 0.1)
    
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:

            Color(*get_color_from_hex('#D8F3EB'))
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )
            Color(*get_color_from_hex('#0F7055'))
            Line(
                rounded_rectangle=[
                    self.x, 
                    self.y, 
                    self.width, 
                    self.height, 
                    dp(10)
                ],
                width=1.2
            )
    
    def update_rect(self, *args):
        """Update the input's background canvas with proper contrast."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=[1, 1, 1, 1])  
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            
            Color(rgba=get_secondary_color())
            Line(rounded_rectangle=[self.x, self.y, self.width, self.height, dp(10)], width=1.2)

class LabeledInput(BoxLayout):
    """
    A text input with a label above it and proper styling.
    """
    label_text = StringProperty("")
    hint_text = StringProperty("")
    text = StringProperty("")
    
    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(80))
        kwargs.setdefault("spacing", dp(5))
        
        super(LabeledInput, self).__init__(**kwargs)
        
        # label
        self.label = Label(
            text=self.label_text,
            size_hint_y=None,
            height=dp(25),
            font_size=sp(FONT_SIZE_MEDIUM),
            color=get_text_primary_color(),
            halign="center",
            valign="bottom", 
            text_size=(None, dp(25))
        )


        with self.label.canvas.before:
            Color(rgba=[0, 0, 0, 0])
            self.label_rect = RoundedRectangle(
                pos=self.label.pos,
                size=self.label.size,
                radius=[dp(10)]
            )

        self.label.bind(pos=self._update_label_rect, size=self._update_label_rect)

        # input
        self.text_input = StyledTextInput(
            hint_text=self.hint_text,
            text=self.text,
            size_hint_y=None,
            height=dp(45))
        
        self.add_widget(self.label)
        self.add_widget(self.text_input)
        
        self.bind(
            label_text=self.update_label,
            hint_text=self.update_hint,
            text=self.update_text
        )
        self.text_input.bind(text=self.on_text_change)
    
    def update_label(self, instance, value):
        self.label.text = value

    def _update_label_rect(self, *args):
        self.label_rect.pos = self.label.pos
        self.label_rect.size = self.label.size
    
    def update_hint(self, instance, value):
        self.text_input.hint_text = value
    
    def update_text(self, instance, value):
        if self.text_input.text != value:
            self.text_input.text = value
    
    def on_text_change(self, instance, value):
        if self.text != value:
            self.text = value
    
    def on_size(self, *args):
        self.label.text_size = (self.width, None)