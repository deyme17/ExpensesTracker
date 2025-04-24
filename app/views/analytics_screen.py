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
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line, Triangle
from datetime import datetime, timedelta

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
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        with self.canvas:
            Color(0.04, 0.25, 0.21, 1)
            Rectangle(pos=self.pos, size=self.size)

class LineChartWidget(Widget):
    def __init__(self, data=None, **kwargs):
        super(LineChartWidget, self).__init__(**kwargs)
        self.data = data or []
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        with self.canvas:
            Color(0.04, 0.25, 0.21, 1)
            Rectangle(pos=self.pos, size=self.size)

class PieChartWidget(Widget):
    def __init__(self, data=None, **kwargs):
        super(PieChartWidget, self).__init__(**kwargs)
        self.data = data or []
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        with self.canvas:
            Color(0.04, 0.25, 0.21, 1)
            Rectangle(pos=self.pos, size=self.size)

class AnalyticsScreen(BaseScreen):
    current_chart_type = StringProperty('histogram')
    avg_value = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(0)
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)
    current_type = StringProperty('Витрати')
    
    expense_dark_color = get_color_from_hex('#A83C36')  
    income_dark_color = get_color_from_hex('#35884D')  
    
    def __init__(self, **kwargs):
        super(AnalyticsScreen, self).__init__(**kwargs)
        self.name = 'statistics'
        self.chart_data = [
            {'name': 'Січ', 'value': 4000, 'month': 1},
            {'name': 'Лют', 'value': 3000, 'month': 2},
            {'name': 'Бер', 'value': 6000, 'month': 3},
            {'name': 'Кві', 'value': 8000, 'month': 4},
            {'name': 'Тра', 'value': 5000, 'month': 5},
            {'name': 'Чер', 'value': 7000, 'month': 6}
        ]
        
        now = datetime.now()
        self.start_date = datetime(now.year - 1, 1, 1)
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
        if not self.start_date or not self.end_date:
            return self.chart_data
        
        return [item for item in self.chart_data 
                if self.start_date.month <= item['month'] <= self.end_date.month]
    
    def _update_stats(self):
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
    
    def show_filter(self):
        modal = ModalView(
            size_hint=(0.8, 0.65),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )

        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=[dp(15), dp(15), dp(15), dp(15)],
            opacity=0
        )

        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(20)])

        content.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(
            text='Фільтр даних',
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )

        date_section = BoxLayout(
            orientation='vertical',
            spacing=dp(6),
            size_hint_y=None,
            height=dp(120)
        )

        date_rect = RoundedRectangle(pos=date_section.pos, size=date_section.size, radius=[dp(12)])
        with date_section.canvas.before:
            Color(rgba=get_color_from_hex('#095045'))
            date_rect

        def update_date_rect(instance, value):
            date_rect.pos = instance.pos
            date_rect.size = instance.size

        date_section.bind(pos=update_date_rect, size=update_date_rect)

        date_title = Label(
            text="Інтервал дат:",
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        date_section.add_widget(date_title)

        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]

        current_year = datetime.now().year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]

        last_year = datetime(current_year - 1, 1, 1)

        date_from_row = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(4))
        date_from_label = Label(
            text="З:",
            size_hint=(None, 1),
            width=dp(20),
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16)
        )
        date_from_row.add_widget(date_from_label)

        start_day_spinner = Spinner(
            text=str(last_year.day).zfill(2),
            values=days,
            size_hint=(0.3, 1),
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )

        start_month_spinner = Spinner(
            text=str(last_year.month).zfill(2),
            values=months,
            size_hint=(0.3, 1),
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )

        start_year_spinner = Spinner(
            text=str(last_year.year),
            values=years,
            size_hint=(0.4, 1),
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )

        date_from_row.add_widget(start_day_spinner)
        date_from_row.add_widget(start_month_spinner)
        date_from_row.add_widget(start_year_spinner)

        date_to_row = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(4))

        date_to_label = Label(
            text="До:",
            size_hint=(None, 1),
            width=dp(20),
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16)
        )
        date_to_row.add_widget(date_to_label)

        end_day_spinner = Spinner(
            text=str(datetime.now().day).zfill(2),
            values=days,
            size_hint=(0.3, 1),
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )

        end_month_spinner = Spinner(
            text=str(datetime.now().month).zfill(2),
            values=months,
            size_hint=(0.3, 1),
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )

        end_year_spinner = Spinner(
            text=str(current_year),
            values=years,
            size_hint=(0.4, 1),
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )

        date_to_row.add_widget(end_day_spinner)
        date_to_row.add_widget(end_month_spinner)
        date_to_row.add_widget(end_year_spinner)

        date_section.add_widget(date_from_row)
        date_section.add_widget(date_to_row)

        type_label = Label(
            text='Тип:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )

        type_spinner = Spinner(
            text='Витрати',
            values=['Витрати', 'Доходи'],
            size_hint_y=None,
            height=dp(45),
            background_normal='',
            background_down='',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            bold=True,
            font_size=sp(16),
            option_cls=SpinnerOption
        )

        class StyledButton(Button):
            def __init__(self, **kwargs):
                super(StyledButton, self).__init__(**kwargs)
                self.background_normal = ''
                self.background_down = ''
                self.background_color = (0, 0, 0, 0)
                self.color = get_color_from_hex('#0A4035')
                self.bold = True
                self.font_size = sp(16)
                self.bind(pos=self.update_rect, size=self.update_rect)
                Clock.schedule_once(lambda dt: self.update_rect(), 0)

            def update_rect(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

        reset_button = StyledButton(text='Скинути')
        apply_button = StyledButton(text='Застосувати')

        reset_button.bind(on_press=lambda x: self.reset_filter(
            type_spinner, None,
            start_day_spinner, start_month_spinner, start_year_spinner,
            end_day_spinner, end_month_spinner, end_year_spinner
        ))
        apply_button.bind(on_press=lambda x: self.apply_filter(
            type_spinner.text, None,
            f"{start_day_spinner.text}.{start_month_spinner.text}.{start_year_spinner.text}",
            f"{end_day_spinner.text}.{end_month_spinner.text}.{end_year_spinner.text}",
            modal
        ))

        buttons_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(15))
        buttons_box.add_widget(reset_button)
        buttons_box.add_widget(apply_button)

        content.add_widget(title_label)
        content.add_widget(date_section)
        content.add_widget(type_label)
        content.add_widget(type_spinner)
        content.add_widget(Widget())
        content.add_widget(buttons_box)

        modal.add_widget(content)
        modal.open()
        Animation(opacity=1, d=0.3).start(content)

    def reset_filter(self, type_spinner, category_spinner,
                    start_day_spinner, start_month_spinner, start_year_spinner,
                    end_day_spinner, end_month_spinner, end_year_spinner):
        type_spinner.text = 'Витрати'
        if category_spinner:
            category_spinner.text = 'Витрати'

        current_year = datetime.now().year
        start_day_spinner.text = '01'
        start_month_spinner.text = '01'
        start_year_spinner.text = str(current_year - 1)

        end_day_spinner.text = str(datetime.now().day).zfill(2)
        end_month_spinner.text = str(datetime.now().month).zfill(2)
        end_year_spinner.text = str(current_year)

    def apply_filter(self, type_filter, category_filter, start_date, end_date, modal):
        try:
            modal.dismiss()
            self.current_type = type_filter

            try:
                start_day, start_month, start_year = start_date.split('.')
                self.start_date = datetime(int(start_year), int(start_month), int(start_day))
            except:
                self.start_date = datetime(datetime.now().year - 1, 1, 1)

            try:
                end_day, end_month, end_year = end_date.split('.')
                self.end_date = datetime(int(end_year), int(end_month), int(end_day))
            except:
                self.end_date = datetime.now()

            self._update_stats()
            self._update_chart()
            self.show_success_message("Фільтр застосовано")

        except Exception as e:
            self.show_error_message(f"Помилка фільтрації: {str(e)}")
    
    def _update_rect(self, instance, value):
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size
    
    def show_error_message(self, message):
        label = Label(
            text=message,
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16),
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))

        popup = Popup(
            title='Помилка',
            content=label,
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )

        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#8B0000'))
            background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])

        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size

        popup.bind(pos=update_rects, size=update_rects)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def show_success_message(self, message):
        label = Label(
            text=message,
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16),
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))

        popup = Popup(
            title='Успіх',
            content=label,
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )

        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])

        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size

        popup.bind(pos=update_rects, size=update_rects)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    
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