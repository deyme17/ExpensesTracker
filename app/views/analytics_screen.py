from app.views.screens import BaseScreen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line

# Load kv file
Builder.load_file('kv/analytics_screen.kv')

class HistogramWidget(Widget):
    def __init__(self, data=None, **kwargs):
        super(HistogramWidget, self).__init__(**kwargs)
        self.data = data or []
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        with self.canvas:
            Color(0.04, 0.25, 0.21, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            Color(0.7, 0.7, 0.7, 1)
            Line(points=[self.x + dp(40), self.y + dp(20), 
                         self.x + dp(40), self.y + self.height - dp(20)])
            Line(points=[self.x + dp(40), self.y + dp(20), 
                         self.x + self.width - dp(20), self.y + dp(20)])
            
            max_value = max([item['value'] for item in self.data])
            bar_width = (self.width - dp(70)) / len(self.data)
            
            for i, item in enumerate(self.data):
                bar_height = (item['value'] / max_value) * (self.height - dp(50))
                x1 = self.x + dp(50) + i * bar_width
                y1 = self.y + dp(20)
                
                Color(*get_color_from_hex('#FF7043')[:3], 1)
                Rectangle(pos=(x1, y1), size=(bar_width * 0.7, bar_height))
                
                label = Label(
                    text=item['name'],
                    size=(bar_width, dp(20)),
                    pos=(x1, self.y),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size='10sp'
                )
                self.add_widget(label)
            
            for i in range(5):
                value = int((i / 4) * max_value)
                y_pos = self.y + dp(20) + (i / 4) * (self.height - dp(50))
                
                Color(0.5, 0.5, 0.5, 0.3)
                Line(points=[self.x + dp(40), y_pos, self.x + self.width - dp(20), y_pos])
                
                label = Label(
                    text=str(value),
                    size=(dp(35), dp(20)),
                    pos=(self.x, y_pos - dp(10)),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size='10sp'
                )
                self.add_widget(label)

class LineChartWidget(Widget):
    def __init__(self, data=None, **kwargs):
        super(LineChartWidget, self).__init__(**kwargs)
        self.data = data or []
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        with self.canvas:
            Color(0.04, 0.25, 0.21, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            Color(0.7, 0.7, 0.7, 1)
            Line(points=[self.x + dp(40), self.y + dp(20), 
                         self.x + dp(40), self.y + self.height - dp(20)])
            Line(points=[self.x + dp(40), self.y + dp(20), 
                         self.x + self.width - dp(20), self.y + dp(20)])
            
            max_value = max([item['value'] for item in self.data])
            points = []
            x_step = (self.width - dp(70)) / (len(self.data) - 1) if len(self.data) > 1 else 0
            
            for i, item in enumerate(self.data):
                x = self.x + dp(50) + i * x_step
                y = self.y + dp(20) + (item['value'] / max_value) * (self.height - dp(50))
                points.extend([x, y])
                
                label = Label(
                    text=item['name'],
                    size=(x_step, dp(20)),
                    pos=(x - x_step/2, self.y),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size='10sp'
                )
                self.add_widget(label)
                
                Color(*get_color_from_hex('#FFB74D')[:3], 1)
                Ellipse(pos=(x - dp(4), y - dp(4)), size=(dp(8), dp(8)))
            
            Color(*get_color_from_hex('#FFB74D')[:3], 1)
            Line(points=points, width=dp(2))
            
            for i in range(5):
                value = int((i / 4) * max_value)
                y_pos = self.y + dp(20) + (i / 4) * (self.height - dp(50))
                
                Color(0.5, 0.5, 0.5, 0.3)
                Line(points=[self.x + dp(40), y_pos, self.x + self.width - dp(20), y_pos])
                
                label = Label(
                    text=str(value),
                    size=(dp(35), dp(20)),
                    pos=(self.x, y_pos - dp(10)),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size='10sp'
                )
                self.add_widget(label)

class PieChartWidget(Widget):
    def __init__(self, data=None, **kwargs):
        super(PieChartWidget, self).__init__(**kwargs)
        self.data = data or []
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        self.clear_widgets()
        
        with self.canvas:
            Color(0.04, 0.25, 0.21, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            total = sum([item['value'] for item in self.data])
            colors = [
                get_color_from_hex('#FF7043'),
                get_color_from_hex('#FFB74D'),
                get_color_from_hex('#66BB6A'),
                get_color_from_hex('#42A5F5'),
                get_color_from_hex('#EC407A'),
                get_color_from_hex('#AB47BC')
            ]
            
            center_x = self.x + self.width * 0.35
            center_y = self.y + self.height * 0.5
            radius = min(self.width, self.height) * 0.35
            start_angle = 0
            
            for i, item in enumerate(self.data):
                angle_size = item['value'] / total * 360
                Color(*colors[i % len(colors)][:3], 1)
                self._draw_sector(center_x, center_y, radius, start_angle, start_angle + angle_size)
                start_angle += angle_size
            
            legend_x = self.x + self.width * 0.65
            legend_y = self.y + self.height * 0.8
            
            for i, item in enumerate(self.data):
                Color(*colors[i % len(colors)][:3], 1)
                Rectangle(pos=(legend_x, legend_y - i * dp(25)), size=(dp(15), dp(15)))
                
                percent = item['value'] / total * 100
                label = Label(
                    text=f"{item['name']}: {percent:.1f}%",
                    size=(dp(150), dp(20)),
                    pos=(legend_x + dp(20), legend_y - i * dp(25) - dp(10)),
                    color=(1, 1, 1, 1),
                    font_size='12sp',
                    halign='left',
                    text_size=(dp(150), dp(20))
                )
                self.add_widget(label)
    
    def _draw_sector(self, center_x, center_y, radius, start_angle, end_angle):
        from math import sin, cos, radians
        
        start_rad = radians(start_angle)
        end_rad = radians(end_angle)
        points = [center_x, center_y]
        points.extend([
            center_x + radius * cos(start_rad),
            center_y + radius * sin(start_rad)
        ])
        
        steps = max(1, int((end_angle - start_angle) / 5))
        for i in range(1, steps + 1):
            angle = start_rad + (end_rad - start_rad) * i / steps
            points.extend([
                center_x + radius * cos(angle),
                center_y + radius * sin(angle)
            ])
        
        self.canvas.add(Color(1, 1, 1, 0.1))
        mesh = self.canvas.add(Line(points=points, width=dp(2), joint='round', close=True))

class StatisticsScreen(BaseScreen):
    current_chart_type = StringProperty('histogram')
    avg_value = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(StatisticsScreen, self).__init__(**kwargs)
        self.name = 'statistics'
        self.chart_data = [
            {'name': 'Січ', 'value': 4000, 'month': 1},
            {'name': 'Лют', 'value': 3000, 'month': 2},
            {'name': 'Бер', 'value': 6000, 'month': 3},
            {'name': 'Кві', 'value': 8000, 'month': 4},
            {'name': 'Тра', 'value': 5000, 'month': 5},
            {'name': 'Чер', 'value': 7000, 'month': 6}
        ]
        
        self._update_stats()
    
    def on_enter(self):
        Clock.schedule_once(self._update_chart, 0.1)
    
    def change_chart_type(self, chart_type):
        if self.current_chart_type == chart_type:
            return
            
        self.current_chart_type = chart_type
        self.graph_container.opacity = 0
        
        def update_and_show(dt):
            self._update_chart()
            Animation(opacity=1, d=0.5).start(self.graph_container)
            
        Clock.schedule_once(update_and_show, 0.3)
    
    def _update_chart(self, *args):
        self.graph_container.clear_widgets()
        
        if self.current_chart_type == 'histogram':
            chart = HistogramWidget(data=self.chart_data)
        elif self.current_chart_type == 'line':
            chart = LineChartWidget(data=self.chart_data)
        elif self.current_chart_type == 'pie':
            chart = PieChartWidget(data=self.chart_data)
        else:
            chart = Widget()
        
        self.graph_container.add_widget(chart)
    
    def _update_stats(self):
        values = [item['value'] for item in self.chart_data]
        self.avg_value = sum(values) / len(values)
        self.min_value = min(values)
        self.max_value = max(values)
    
    def go_to_transactions(self):
        self.switch_screen('main_screen', 'right')
    
    def show_menu(self):
        popup = Popup(
            title='Меню',
            size_hint=(0.7, 0.2),
            background='',
            background_color=(0, 0, 0, 0))
        
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10))
        
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
            
            Color(rgba=get_color_from_hex('#FF7043'))
            RoundedRectangle(
                pos=(popup.x + dp(10), popup.y + popup.height - dp(3)),
                size=(popup.width - dp(20), dp(3)),
                radius=[dp(1.5)]
            )
        
        popup.title_color = get_color_from_hex('#FFFFFF')
        popup.title_size = sp(18)
        
        exit_btn = Button(
            text='Вихід',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16))
        exit_btn.bind(on_press=lambda x: [popup.dismiss(), self.exit_app()])
        content.add_widget(exit_btn)
        
        popup.content = content
        popup.open()
    
    def exit_app(self):
        from kivy.app import App
        App.get_running_app().stop()