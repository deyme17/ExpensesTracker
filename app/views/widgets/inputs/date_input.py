from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.metrics import dp, sp
from kivy.clock import Clock
from datetime import datetime
from app.views.widgets.inputs.custom_spinner import CustomSpinner

from app.utils.theme import FONT_SIZE_MEDIUM


class DateInput(BoxLayout):
    """
    A compound widget for date input with day/month/year spinners.
    """
    hint_text = StringProperty("")
    day = StringProperty("01")
    month = StringProperty("01")
    year = StringProperty("")
    date_text = StringProperty("")
    
    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(45))
        kwargs.setdefault("spacing", dp(5))

        super(DateInput, self).__init__(**kwargs)

        now = datetime.now()
        self.day = now.strftime("%d")
        self.month = now.strftime("%m")
        self.year = now.strftime("%Y")

        days = [str(i).zfill(2) for i in range(1, 32)]
        self.day_spinner = CustomSpinner(
            text=self.day,
            values=days,
            size_hint=(0.33, 1),
            padding_x=dp(2)
        )

        months = [str(i).zfill(2) for i in range(1, 13)]
        self.month_spinner = CustomSpinner(
            text=self.month,
            values=months,
            size_hint=(0.33, 1),
            padding_x=dp(2)
        )

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
        self.day = value
        self._update_date_text()
    
    def _on_month_changed(self, instance, value):
        self.month = value
        self._update_date_text()
    
    def _on_year_changed(self, instance, value):
        self.year = value
        self._update_date_text()
    
    def _update_date_text(self):
        self.date_text = f"{self.day}.{self.month}.{self.year}"


class LabeledDateInput(BoxLayout):
    """
    A date input with a label above it.
    """
    label_text = StringProperty("")
    date_text = StringProperty("")
    
    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(75))
        kwargs.setdefault("spacing", dp(5))
        
        super(LabeledDateInput, self).__init__(**kwargs)
        
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
        self.date_text = self.date_input.date_text
    
    def _update_label_text(self, instance, value):
        """Update the label text when the property changes."""
        self.label.text = value
    
    def _update_date_text(self, instance, value):
        """Update the date input when the date_text property changes."""
        if value:
            try:
                day, month, year = value.split(".")
                self.date_input.day_spinner.text = day
                self.date_input.month_spinner.text = month
                self.date_input.year_spinner.text = year
            except ValueError:
                pass
    
    def _on_date_changed(self, instance, value):
        """Update the date_text property when the date input changes."""
        self.date_text = value