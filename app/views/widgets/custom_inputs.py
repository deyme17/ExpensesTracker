from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Triangle, Line
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from datetime import datetime

from app.utils.theme import (
    get_text_dark_color, get_secondary_color, get_text_primary_color,
    get_primary_color, FONT_SIZE_MEDIUM
)


class StyledTextInput(TextInput):
    """
    A styled text input with dark visible text and proper padding.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', (0, 0, 0, 0)) 
        kwargs.setdefault('foreground_color', get_color_from_hex('#212121')) 
        kwargs.setdefault('cursor_color', get_color_from_hex('#212121'))  
        kwargs.setdefault('hint_text_color', get_color_from_hex('#B0BEC5'))  
        kwargs.setdefault('font_size', sp(16))
        kwargs.setdefault('multiline', False)
        kwargs.setdefault('padding', [dp(15), dp(12), dp(15), dp(12)])
        kwargs.setdefault('write_tab', False)
        
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
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(80))
        kwargs.setdefault('spacing', dp(5))
        
        super(LabeledInput, self).__init__(**kwargs)
        
        # label
        self.label = Label(
            text=self.label_text,
            size_hint_y=None,
            height=dp(25),
            font_size=sp(FONT_SIZE_MEDIUM),
            color=get_text_primary_color(),
            halign='center',
            valign='bottom', 
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

class CustomSpinner(Spinner):
    """
    A styled spinner (dropdown) with rounded corners and custom arrow.
    """
    selected_value = StringProperty("")
    padding_x = NumericProperty(dp(15))
    
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', (0, 0, 0, 0))
        kwargs.setdefault('color', get_text_dark_color())
        kwargs.setdefault('bold', True)
        kwargs.setdefault('font_size', sp(FONT_SIZE_MEDIUM))
        kwargs.setdefault('option_cls', SpinnerOption)
        
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
    A spinner with a label above it.
    """
    label_text = StringProperty("")
    values = ListProperty([])
    selected = StringProperty("")
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(75))
        kwargs.setdefault('spacing', dp(5))
        
        super(LabeledSpinner, self).__init__(**kwargs)
        
        # label
        self.label = Label(
            text=self.label_text,
            size_hint_y=None,
            height=dp(25),
            font_size=sp(FONT_SIZE_MEDIUM),
            halign='left',
            valign='bottom',
            text_size=(None, dp(25))
        )
        
        # spinner
        self.spinner = CustomSpinner(
            text=self.selected if self.selected else (self.values[0] if self.values else ""),
            values=self.values,
            size_hint_y=None,
            height=dp(45)
        )
        
        self.add_widget(self.label)
        self.add_widget(self.spinner)
        
        self.bind(label_text=self._update_label_text)
        self.bind(values=self._update_values)
        self.bind(selected=self._update_selected)
       
        self.spinner.bind(text=self._on_spinner_changed)
    
    def _update_label_text(self, instance, value):
        """Update the label text when the property changes."""
        self.label.text = value
    
    def _update_values(self, instance, value):
        """Update the spinner values when the property changes."""
        self.spinner.values = value
        
        if self.selected and self.selected not in value:
            if value:
                self.selected = value[0]
            else:
                self.selected = ""
    
    def _update_selected(self, instance, value):
        """Update the spinner text when the selected property changes."""
        self.spinner.text = value
    
    def _on_spinner_changed(self, instance, value):
        """Update the selected property when the spinner changes."""
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
        self.halign = 'center'

class DateInput(BoxLayout):
    """
    A compound widget for date input with day/month/year spinners.
    """
    day = StringProperty("01")
    month = StringProperty("01")
    year = StringProperty("")
    date_text = StringProperty("")
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'horizontal')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(45))
        kwargs.setdefault('spacing', dp(5))

        super(DateInput, self).__init__(**kwargs)

        now = datetime.now()
        # current date
        self.day = now.strftime("%d")
        self.month = now.strftime("%m")
        self.year = now.strftime("%Y")

        # day spinner
        days = [str(i).zfill(2) for i in range(1, 32)]
        self.day_spinner = CustomSpinner(
            text=self.day,
            values=days,
            size_hint=(0.33, 1),
            padding_x=dp(2)
        )

        # month spinner
        months = [str(i).zfill(2) for i in range(1, 13)]
        self.month_spinner = CustomSpinner(
            text=self.month,
            values=months,
            size_hint=(0.33, 1),
            padding_x=dp(2)
        )

        # year spinner
        current_year = now.year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]
        self.year_spinner = CustomSpinner(
            text=self.year,
            values=years,
            size_hint=(0.33, 1),
            padding_x=dp(5)
        )

        self.add_widget(self.day_spinner)
        self.add_widget(self.month_spinner)
        self.add_widget(self.year_spinner)

        self.day_spinner.bind(text=self._on_day_changed)
        self.month_spinner.bind(text=self._on_month_changed)
        self.year_spinner.bind(text=self._on_year_changed)

        self._update_date_text()
    
    def _on_day_changed(self, instance, value):
        """Update the day property when the spinner changes."""
        self.day = value
        self._update_date_text()
    
    def _on_month_changed(self, instance, value):
        """Update the month property when the spinner changes."""
        self.month = value
        self._update_date_text()
    
    def _on_year_changed(self, instance, value):
        """Update the year property when the spinner changes."""
        self.year = value
        self._update_date_text()
    
    def _update_date_text(self):
        """Update the date_text property with the current date components."""
        self.date_text = f"{self.day}.{self.month}.{self.year}"

class LabeledDateInput(BoxLayout):
    """
    A date input with a label above it.
    """
    label_text = StringProperty("")
    date_text = StringProperty("")
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(75))
        kwargs.setdefault('spacing', dp(5))
        
        super(LabeledDateInput, self).__init__(**kwargs)
        
        # label
        self.label = Label(
            text=self.label_text,
            size_hint_y=None,
            height=dp(25),
            font_size=sp(FONT_SIZE_MEDIUM),
            halign='left',
            valign='bottom',
            text_size=(None, dp(25))
        )
        
        # date input
        self.date_input = DateInput(
            size_hint_y=None,
            height=dp(45)
        )
        
        self.date_input.day_spinner.padding_x = dp(25)
        self.date_input.month_spinner.padding_x = dp(25)
        self.date_input.year_spinner.padding_x = dp(25)
        
        self.add_widget(self.label)
        self.add_widget(self.date_input)
        
        self.bind(label_text=self._update_label_text)
        self.bind(date_text=self._update_date_text)
        
        self.date_input.bind(date_text=self._on_date_changed)
    
    def _update_label_text(self, instance, value):
        """Update the label text when the property changes."""
        self.label.text = value
    
    def _update_date_text(self, instance, value):
        """Update the date input when the date_text property changes."""
        if value:
            try:
                day, month, year = value.split('.')
                self.date_input.day = day
                self.date_input.month = month
                self.date_input.year = year
            except ValueError:
                pass
    
    def _on_date_changed(self, instance, value):
        """Update the date_text property when the date input changes."""
        self.date_text = value