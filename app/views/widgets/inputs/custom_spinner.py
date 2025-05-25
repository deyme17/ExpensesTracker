from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Triangle
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from datetime import datetime

from app.utils.theme import (
    get_text_dark_color, get_secondary_color, get_text_primary_color,
    get_primary_color, FONT_SIZE_MEDIUM
)

class CustomSpinner(Spinner):
    """
    A styled spinner (dropdown) with rounded corners and custom arrow.
    """
    selected_value = StringProperty("")
    padding_x = NumericProperty(dp(15))
    label_text = StringProperty("")
    selected = StringProperty("")  

    def __init__(self, **kwargs):
        self.display_transform = kwargs.pop("display_transform", lambda x: x)
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("color", get_text_dark_color())
        kwargs.setdefault("bold", True)
        kwargs.setdefault("font_size", sp(FONT_SIZE_MEDIUM))
        kwargs.setdefault("option_cls", SpinnerOption)
        
        super(CustomSpinner, self).__init__(**kwargs)
        
        if self.text:
            self.selected_value = self.text
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(text=self._on_text_changed)
        Clock.schedule_once(lambda dt: self.update_rect(), 0)
    
    def update_rect(self, *args):
        """Update the spinner's background canvas with dropdown arrow."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_secondary_color())
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            Color(rgba=get_primary_color())
            x = self.x + self.width - self.padding_x
            y = self.y + self.height / 2 - dp(2)
            Triangle(points=[
                x, y + dp(5),
                x + dp(10), y + dp(5),
                x + dp(5), y - dp(5)
            ])
    
    def _on_text_changed(self, instance, value):
        """Update the selected value when the text changes."""
        self.selected_value = value


class LabeledSpinner(BoxLayout):
    """
    A spinner with a label above it that supports localization via displayed_value.
    """
    label_text = StringProperty("")
    values = ListProperty([])
    selected = StringProperty("")
    displayed_value = ObjectProperty(lambda x: x)

    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(75))
        kwargs.setdefault("spacing", dp(5))

        super(LabeledSpinner, self).__init__(**kwargs)

        self._display_to_key = {}

        # label
        self.label = Label(
            text=self.label_text,
            size_hint_y=None,
            height=dp(25),
            font_size=sp(FONT_SIZE_MEDIUM),
            halign="left",
            valign="bottom",
            text_size=(None, dp(25))
        )

        # spinner
        self.spinner = CustomSpinner(
            text="",
            values=[],
            size_hint_y=None,
            height=dp(45)
        )

        self.spinner.bind(text=self._on_spinner_changed)

        self.add_widget(self.label)
        self.add_widget(self.spinner)

        self.bind(label_text=self._update_label_text)
        self.bind(values=self._update_values)
        self.bind(selected=self._update_selected)
        self.bind(displayed_value=self._update_displayed_values)

    def _update_label_text(self, instance, value):
        self.label.text = value

    def _update_values(self, instance, value):
        self._update_displayed_values()

    def _update_displayed_values(self, *args):
        self._display_to_key = {self.displayed_value(v): v for v in self.values}
        self.spinner.values = list(self._display_to_key.keys())
        self._update_selected(self, self.selected)

    def _update_selected(self, instance, value):
        for display, key in self._display_to_key.items():
            if key == value:
                self.spinner.text = display
                break

    def _on_spinner_changed(self, instance, value):
        if value in self._display_to_key:
            self.selected = self._display_to_key[value]
        else:
            self.selected = value


class SpinnerOption(Button):
    """
    Custom styled option for the spinner dropdown.
    """
    def __init__(self, **kwargs):
        super(SpinnerOption, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = get_secondary_color()
        self.color = get_text_dark_color()
        self.font_size = sp(FONT_SIZE_MEDIUM)
        self.halign = "center"