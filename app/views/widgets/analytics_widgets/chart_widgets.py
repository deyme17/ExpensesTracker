from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, BooleanProperty, StringProperty, ObjectProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock

from app.utils.theme import (
    get_primary_color, get_income_color, get_expense_color,
)


class BaseChartWidget(Widget):
    """Base class for chart widgets."""
    data = ListProperty([])
    type = ObjectProperty(False)
    
    def __init__(self, **kwargs):
        super(BaseChartWidget, self).__init__(**kwargs)
        self.bind(data=self.update_canvas)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        Clock.schedule_once(lambda dt: self.update_canvas(), 0.1)
    
    def update_canvas(self, *args):
        """Update the widget's canvas. Override in subclasses."""
        self.canvas.clear()
        if not self.data:
            return
        
        # Draw background
        with self.canvas:
            Color(*get_primary_color())
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
    
    def get_color(self):
        """Get the main color for the chart based on whether it's for income or expenses."""
        return get_income_color() if self.type else get_expense_color()


class BarChartWidget(BaseChartWidget):
    """Widget for displaying a bar chart."""
    
    def update_canvas(self, *args):
        """Update the bar chart canvas."""
        super(BarChartWidget, self).update_canvas(*args)
        if not self.data:
            return
        return # TODO


class PieChartWidget(BaseChartWidget):
    """Widget for displaying a pie chart."""
    
    def update_canvas(self, *args):
        """Update the pie chart canvas."""
        super(PieChartWidget, self).update_canvas(*args)
        if not self.data:
            return
        return # TODO


class LineChartWidget(BaseChartWidget):
    """Widget for displaying a line chart."""
    
    def update_canvas(self, *args):
        """Update the line chart canvas."""
        super(LineChartWidget, self).update_canvas(*args)
        if not self.data:
            return
        
        return # TODO

class ChartContainer(BoxLayout):
    """Container for charts with title and legend."""
    chart_type = StringProperty("histogram")
    data = ListProperty([])
    title = StringProperty('')
    type = ObjectProperty(False)
    
    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("spacing", dp(10))
        kwargs.setdefault("padding", dp(5))
        
        super(ChartContainer, self).__init__(**kwargs)
        
        self.chart_widget = Widget(size_hint_y=1)
        
        self.add_widget(self.chart_widget)
        
        self.bind(chart_type=self._update_chart)
        self.bind(data=self._update_data)
        self.bind(type=self._update_income)
      
        Clock.schedule_once(lambda dt: self._update_chart(), 0.1)
    
    def _update_chart(self, *args):
        """Update the chart widget based on chart_type."""
        # clear
        self.remove_widget(self.chart_widget)
        
        if self.chart_type == "histogram":
            self.chart_widget = BarChartWidget(
                data=self.data,
                type=self.type,
                size_hint_y=1
            )
        elif self.chart_type == "pie":
            self.chart_widget = PieChartWidget(
                data=self.data,
                type=self.type,
                size_hint_y=1
            )
        elif self.chart_type == "line":
            self.chart_widget = LineChartWidget(
                data=self.data,
                type=self.type,
                size_hint_y=1
            )
        else:
            self.chart_widget = Widget(size_hint_y=1)
        
        # chart
        self.add_widget(self.chart_widget)
    
    def _update_data(self, instance, value):
        """Update chart data when data property changes."""
        if hasattr(self.chart_widget, "data"):
            self.chart_widget.data = value
    
    def _update_income(self, instance, value):
        """Update type when property changes."""
        if hasattr(self.chart_widget, "type"):
            self.chart_widget.type = value