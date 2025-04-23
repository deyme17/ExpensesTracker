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
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line, Triangle
from datetime import datetime

# Load kv file
Builder.load_file('kv/analytics_screen.kv')

class SpinnerOption(Button):
    def __init__(self, **kwargs):
        super(SpinnerOption, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = get_color_from_hex('#D8F3EB')
        self.color = get_color_from_hex('#0A4035')
        self.font_size = sp(16)
        self.halign = 'center'

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

class DateFilterPopup(Popup):
    def __init__(self, callback, **kwargs):
        super(DateFilterPopup, self).__init__(**kwargs)
        self.title = 'Вибір періоду'
        self.size_hint = (0.85, 0.45)
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.title_color = get_color_from_hex('#FFFFFF')
        self.title_size = sp(18)
        
        self.callback = callback
        
        # Get current date
        current_date = datetime.now()
        day = str(current_date.day).zfill(2)
        month = str(current_date.month).zfill(2)
        year = str(current_date.year)
        
        # Create layout
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20)
        )
        
        # Add background
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#0D5145'))  # Light shade of green
            background_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        
        # Update rectangle positions when popup size changes
        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size
        
        self.bind(pos=update_rects, size=update_rects)
        
        # Date selectors
        date_main_container = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(120)
        )
        
        # "З:" row
        from_row = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(45)
        )
        
        from_label = Label(
            text='З:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            size_hint_x=None,
            width=dp(25)
        )
        
        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        current_year = current_date.year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]
        
        self.from_day_spinner = Spinner(
            text=day,
            values=days,
            size_hint_x=0.27,
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )
        
        self.from_month_spinner = Spinner(
            text=month,
            values=months,
            size_hint_x=0.27,
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )
        
        self.from_year_spinner = Spinner(
            text=year,
            values=years,
            size_hint_x=0.35,
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )
        
        from_row.add_widget(from_label)
        from_row.add_widget(self.from_day_spinner)
        from_row.add_widget(self.from_month_spinner)
        from_row.add_widget(self.from_year_spinner)
        
        # "До:" row
        to_row = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(45)
        )
        
        to_label = Label(
            text='До:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            size_hint_x=None,
            width=dp(25)
        )
        
        self.to_day_spinner = Spinner(
            text=day,
            values=days,
            size_hint_x=0.27,
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )
        
        self.to_month_spinner = Spinner(
            text=month,
            values=months,
            size_hint_x=0.27,
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )
        
        self.to_year_spinner = Spinner(
            text=year,
            values=years,
            size_hint_x=0.35,
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )
        
        to_row.add_widget(to_label)
        to_row.add_widget(self.to_day_spinner)
        to_row.add_widget(self.to_month_spinner)
        to_row.add_widget(self.to_year_spinner)
        
        date_main_container.add_widget(from_row)
        date_main_container.add_widget(to_row)
        
        # Buttons row
        buttons_container = BoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(50),
            padding=[0, dp(10), 0, 0]
        )
        
        cancel_btn = Button(
            text='Скасувати',
            size_hint_x=0.5,
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16)
        )
        cancel_btn.bind(on_release=self.dismiss)
        
        apply_btn = Button(
            text='Застосувати',
            size_hint_x=0.5,
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16)
        )
        apply_btn.bind(on_release=self.apply_filter)
        
        buttons_container.add_widget(cancel_btn)
        buttons_container.add_widget(apply_btn)
        
        # Add all sections to main layout
        content_layout.add_widget(date_main_container)
        content_layout.add_widget(buttons_container)
        
        self.content = content_layout
    
    def apply_filter(self, *args):
        try:
            # Get selected dates from spinners
            start_date = datetime(
                int(self.from_year_spinner.text),
                int(self.from_month_spinner.text),
                int(self.from_day_spinner.text)
            )
            
            end_date = datetime(
                int(self.to_year_spinner.text),
                int(self.to_month_spinner.text),
                int(self.to_day_spinner.text)
            )
            
            if start_date <= end_date:
                self.callback(start_date, end_date)
                self.dismiss()
            else:
                # Simple error handling
                print("Помилка: початкова дата повинна бути раніше кінцевої")
        except Exception as e:
            # Handle invalid date inputs
            print(f"Помилка застосування фільтру: {e}")

class StatisticsScreen(BaseScreen):
    current_chart_type = StringProperty('histogram')
    avg_value = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(0)
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)
    
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
        
        # Set default date range to current month
        now = datetime.now()
        self.start_date = datetime(now.year, now.month, 1)
        self.end_date = now
        
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
        
        # Filter data by date range if needed
        filtered_data = self._filter_data_by_date()
        
        if self.current_chart_type == 'histogram':
            chart = HistogramWidget(data=filtered_data)
        elif self.current_chart_type == 'line':
            chart = LineChartWidget(data=filtered_data)
        elif self.current_chart_type == 'pie':
            chart = PieChartWidget(data=filtered_data)
        else:
            chart = Widget()
        
        self.graph_container.add_widget(chart)
    
    def _filter_data_by_date(self):
        # In a real app, you would filter from your database
        if not self.start_date or not self.end_date:
            return self.chart_data
        
        return [item for item in self.chart_data 
                if self.start_date.month <= item['month'] <= self.end_date.month]
    
    def _update_stats(self):
        # Use filtered data for statistics
        filtered_data = self._filter_data_by_date()
        values = [item['value'] for item in filtered_data]
        
        if values:
            self.avg_value = sum(values) / len(values)
            self.min_value = min(values)
            self.max_value = max(values)
        else:
            self.avg_value = 0
            self.min_value = 0
            self.max_value = 0
    
    def show_date_filter(self):
        popup = DateFilterPopup(callback=self.apply_date_filter)
        popup.open()
    
    def apply_date_filter(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._update_stats()
        self._update_chart()
    
    def go_to_transactions(self):
        self.switch_screen('main_screen', 'right')
    
    def show_menu(self):
        popup = Popup(
            title='Меню',
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )

        popup.content = content

        with popup.canvas.before:
            color = Color(rgba=get_color_from_hex('#0A4035'))
            background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])

        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size

        popup.bind(pos=update_rects, size=update_rects)
        popup.title_color = get_color_from_hex('#FFFFFF')
        popup.title_size = sp(18)

        class MenuButton(Button):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.color = get_color_from_hex('#0A4035')
                self.font_size = sp(16)
                self.bind(size=self.update_bg, pos=self.update_bg)
                Clock.schedule_once(lambda dt: self.update_bg(), 0)

            def update_bg(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

        logout_btn = MenuButton(
            text='Вийти з акаунту',
            size_hint_y=None,
            height=dp(45)
        )
        logout_btn.bind(on_press=lambda x: [popup.dismiss(), self.logout()])

        exit_btn = MenuButton(
            text='Вихід із програми',
            size_hint_y=None,
            height=dp(45)
        )
        exit_btn.bind(on_press=lambda x: [popup.dismiss(), self.exit_app()])

        content.add_widget(logout_btn)
        content.add_widget(exit_btn)
        popup.content = content
        popup.open()
    
    def exit_app(self):
        from kivy.app import App
        App.get_running_app().stop()