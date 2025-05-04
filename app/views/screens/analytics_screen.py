from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line, Triangle
from kivy.lang import Builder
from datetime import datetime, timedelta

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.chart_widgets import ChartContainer
from app.views.widgets.buttons.styled_button import RoundedButton
from app.views.widgets.buttons.segmented_button import  SegmentedButton
from app.views.widgets.inputs.custom_spinner import CustomSpinner
from app.utils.constants import (
    TRANSACTION_TYPE_INCOME, TRANSACTION_TYPE_EXPENSE,
    CHART_TYPE_HISTOGRAM, CHART_TYPE_PIE, CHART_TYPE_LINE
)
from app.utils.formatters import format_amount, format_date_range
from app.utils.theme import (
    get_primary_color, get_text_primary_color,
)

# Load kv file
Builder.load_file('kv/analytics_screen.kv')

class AnalyticsScreen(BaseScreen):
    """
    Screen for displaying analytics data.
    
    This screen shows various charts and statistics for transactions.
    """
    current_chart_type = StringProperty(CHART_TYPE_HISTOGRAM)
    avg_value = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(0)
    total_value = NumericProperty(0)
    count_value = NumericProperty(0)
    top_category = StringProperty("Немає даних")
    current_type = StringProperty(TRANSACTION_TYPE_EXPENSE)
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)
    date_range_text = StringProperty("")
    controller = ObjectProperty(None)
    
    expense_dark_color = get_color_from_hex('#A83C36')  
    income_dark_color = get_color_from_hex('#35884D')
    
    def __init__(self, **kwargs):
        super(AnalyticsScreen, self).__init__(**kwargs)
        self.name = 'analytics_screen'
    
        now = datetime.now()
        self.start_date = datetime(now.year - 1, 1, 1)
        self.end_date = now
        
        self._update_date_range_text()
    
    def on_enter(self):
        """Called when the screen enters the view."""
        super(AnalyticsScreen, self).on_enter()
        
        if not hasattr(self, '_analytics_loaded') or not self._analytics_loaded:
            Clock.schedule_once(self._load_analytics_data, 0.1)
            self._analytics_loaded = True
    
    def _load_analytics_data(self, dt):
        """Load analytics data from the controller."""
        if not self.controller:
            return
        
        analytics_data = self.controller.get_analytics_data(
            transaction_type=self.current_type,
            start_date=self.start_date,
            end_date=self.end_date
        )
        # update ui
        self.avg_value = analytics_data.get_avg_value()
        self.min_value = analytics_data.get_min_value()
        self.max_value = analytics_data.get_max_value()
        self.total_value = analytics_data.get_total()
        self.count_value = analytics_data.get_count()
        self.top_category = analytics_data.get_top_category()
        
        # update chart
        self._update_chart(analytics_data)
    
    def _update_chart(self, analytics_data=None):
        """Update the chart with current data."""
        if not analytics_data and not self.controller:
            return
        
        self.graph_container.opacity = 0
        
        if not analytics_data:
            analytics_data = self.controller.get_analytics_data(
                transaction_type=self.current_type,
                start_date=self.start_date,
                end_date=self.end_date
            )
        
        self.graph_container.clear_widgets()
   
        chart_data = analytics_data.get_chart_data(self.current_chart_type)

        is_income = self.current_type == TRANSACTION_TYPE_INCOME
        chart = ChartContainer(
            chart_type=self.current_chart_type,
            data=chart_data,
            title=f"{self.current_type} за {self.date_range_text}",
            is_income=is_income
        )

        self.graph_container.add_widget(chart)
  
        Animation(opacity=1, d=0.5).start(self.graph_container)
    
    def change_chart_type(self, chart_type):
        """Change the current chart type."""
        if self.current_chart_type == chart_type:
            return
        
        self.current_chart_type = chart_type
        self.graph_container.opacity = 0
        
        def update_and_show(dt):
            self._update_chart()
            Animation(opacity=1, d=0.5).start(self.graph_container)
        
        Clock.schedule_once(update_and_show, 0.3)
    
    def _update_date_range_text(self):
        """Update the date range text."""
        if not self.start_date or not self.end_date:
            return
        
        self.date_range_text = format_date_range(self.start_date, self.end_date)
    
    def _filter_data_by_date(self):
        """Helper function to filter data by date range."""
        if not self.controller:
            return []
        
        return self.controller.get_analytics_data(
            transaction_type=self.current_type,
            start_date=self.start_date,
            end_date=self.end_date
        ).get_chart_data(self.current_chart_type)
    
    def _update_stats(self):
        """Update statistics from filtered data."""
        if not self.controller:
            return
        
        analytics_data = self.controller.get_analytics_data(
            transaction_type=self.current_type,
            start_date=self.start_date,
            end_date=self.end_date
        )
        
        if analytics_data:
            self.avg_value = analytics_data.get_avg_value()
            self.min_value = analytics_data.get_min_value()
            self.max_value = analytics_data.get_max_value()
            self.total_value = analytics_data.get_total()
            self.count_value = analytics_data.get_count()
            self.top_category = analytics_data.get_top_category()
        else:
            self.avg_value = 0
            self.min_value = 0
            self.max_value = 0
            self.total_value = 0
            self.count_value = 0
            self.top_category = "Немає даних"
    
    def show_filter(self):
        """Show dialog for filtering analytics data."""
        # modal
        modal = ModalView(
            size_hint=(0.8, 0.8),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )
        
        # content
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(15), dp(15), dp(15), dp(15)],
            opacity=0
        )
        
        with content.canvas.before:
            Color(rgba=get_primary_color())
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(20)])
        
        content.bind(size=self._update_rect, pos=self._update_rect)
        
        # title
        title_label = Label(
            text='Фільтр транзакцій',
            font_size=sp(20),
            bold=True,
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )

        # transaction type
        type_label = Label(
            text='Тип:',
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        type_spinner = CustomSpinner(
            text=self.current_type,
            values=['Витрати', 'Доходи'],
            size_hint_y=None,
            height=dp(45),
            padding_x=dp(25)
        )
        
        # date range section
        date_section = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(200),
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        
        with date_section.canvas.before:
            Color(rgba=(0.09, 0.50, 0.45, 1))
            date_rect = RoundedRectangle(pos=date_section.pos, size=date_section.size, radius=[dp(12)])
        
        def update_date_rect(instance, value):
            date_rect.pos = instance.pos
            date_rect.size = instance.size
        
        date_section.bind(pos=update_date_rect, size=update_date_rect)
        
        date_title = Label(
            text="Інтервал дат:",
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        date_section.add_widget(date_title)
        
        # date
        start_date_label = Label(
            text="З:",
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='left',
            size_hint_y=None,
            height=dp(30)
        )
        date_section.add_widget(start_date_label)
        
        from datetime import datetime
        
        # days
        days = [str(i).zfill(2) for i in range(1, 32)]
        
        # months
        months = [str(i).zfill(2) for i in range(1, 13)]
        
        # years
        current_year = datetime.now().year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]
        
        # date spinners
        start_date_row = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(45)
        )
        
        start_day_spinner = CustomSpinner(
            text=str(self.start_date.day).zfill(2),
            values=days,
            size_hint=(0.3, 1),
            padding_x=dp(25)
        )
        
        start_month_spinner = CustomSpinner(
            text=str(self.start_date.month).zfill(2),
            values=months,
            size_hint=(0.3, 1),
            padding_x=dp(25)
        )
        
        start_year_spinner = CustomSpinner(
            text=str(self.start_date.year),
            values=years,
            size_hint=(0.4, 1),
            padding_x=dp(25)
        )
        
        start_date_row.add_widget(start_day_spinner)
        start_date_row.add_widget(start_month_spinner)
        start_date_row.add_widget(start_year_spinner)
        
        date_section.add_widget(start_date_row)
        
        end_date_label = Label(
            text="До:",
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='left',
            size_hint_y=None,
            height=dp(30)
        )
        date_section.add_widget(end_date_label)
        
        end_date_row = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(45)
        )
        
        end_day_spinner = CustomSpinner(
            text=str(self.end_date.day).zfill(2),
            values=days,
            size_hint=(0.3, 1),
            padding_x=dp(25)
        )
        
        end_month_spinner = CustomSpinner(
            text=str(self.end_date.month).zfill(2),
            values=months,
            size_hint=(0.3, 1),
            padding_x=dp(25)
        )
        
        end_year_spinner = CustomSpinner(
            text=str(self.end_date.year),
            values=years,
            size_hint=(0.4, 1),
            padding_x=dp(25)
        )
        
        end_date_row.add_widget(end_day_spinner)
        end_date_row.add_widget(end_month_spinner)
        end_date_row.add_widget(end_year_spinner)
        
        date_section.add_widget(end_date_row)
        
        # buttons
        buttons_box = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10)
        )
        
        reset_button = RoundedButton(
            text='[b]Скинути[/b]',
            bg_color='#445555',
            font_size=sp(12),
            markup=True
        )
        
        close_button = RoundedButton(
            text='[b]Закрити[/b]',
            bg_color='#666666',
            font_size=sp(12),
            markup=True
        )
        
        apply_button = RoundedButton(
            text='[b]Застосувати[/b]',
            bg_color='#0F7055',
            font_size=sp(12),
            markup=True
        )
        
        # bind button actions
        def reset_filter(x):
            type_spinner.text = 'Витрати'
            
            # Reset dates to default
            now = datetime.now()
            last_year = datetime(now.year - 1, 1, 1)
            
            start_day_spinner.text = '01'
            start_month_spinner.text = '01'
            start_year_spinner.text = str(last_year.year)
            
            end_day_spinner.text = str(now.day).zfill(2)
            end_month_spinner.text = str(now.month).zfill(2)
            end_year_spinner.text = str(now.year)
        
        def apply_filter(x):
            try:
                # Update type
                self.current_type = type_spinner.text
                
                # Parse dates
                start_date_text = f"{start_day_spinner.text}.{start_month_spinner.text}.{start_year_spinner.text}"
                end_date_text = f"{end_day_spinner.text}.{end_month_spinner.text}.{end_year_spinner.text}"
                
                # Parse start date
                try:
                    start_day, start_month, start_year = start_date_text.split('.')
                    self.start_date = datetime(int(start_year), int(start_month), int(start_day))
                except:
                    # Default to a year ago
                    now = datetime.now()
                    self.start_date = datetime(now.year - 1, 1, 1)
                
                # Parse end date
                try:
                    end_day, end_month, end_year = end_date_text.split('.')
                    self.end_date = datetime(int(end_year), int(end_month), int(end_day))
                except:
                    # Default to current date
                    self.end_date = datetime.now()
                
                # Update date range text
                self._update_date_range_text()
                
                # Update statistics
                self._update_stats()
                
                # Update chart
                self._update_chart()
                
                # Close modal
                modal.dismiss()
                
                # Show success message
                self.show_success_message("Фільтр застосовано")
                
            except Exception as e:
                self.show_error_message(f"Помилка фільтрації: {str(e)}")
        
        reset_button.bind(on_press=reset_filter)
        close_button.bind(on_press=lambda x: modal.dismiss())
        apply_button.bind(on_press=apply_filter)
        
        buttons_box.add_widget(reset_button)
        buttons_box.add_widget(close_button)
        buttons_box.add_widget(apply_button)
        
        # Add all elements to content
        content.add_widget(title_label)
        content.add_widget(type_label)
        content.add_widget(type_spinner)
        content.add_widget(BoxLayout(size_hint_y=1))  # space
        content.add_widget(BoxLayout(size_hint_y=1))  # space
        content.add_widget(date_section)
        content.add_widget(BoxLayout(size_hint_y=1))  # space
        content.add_widget(buttons_box)
        
        # Add content to modal
        modal.add_widget(content)
        
        # Open modal and animate
        modal.open()
        Animation(opacity=1, d=0.3).start(content)
    
    def _reset_filter(self, type_spinner, start_date_input, end_date_input):
        """Reset filter inputs to default values."""
        type_spinner.text = TRANSACTION_TYPE_EXPENSE
        
        # reset dates
        now = datetime.now()
        last_year = datetime(now.year - 1, 1, 1)
        
        # update start date
        start_date_input.day = '01'
        start_date_input.month = '01'
        start_date_input.year = str(last_year.year)
        
        # Update end date
        end_date_input.day = str(now.day).zfill(2)
        end_date_input.month = str(now.month).zfill(2)
        end_date_input.year = str(now.year)
    
    def _apply_filter(self, type_filter, start_date, end_date, modal):
        """Apply the selected filter."""
        try:
            self.current_type = type_filter
            
            # parse start date
            try:
                start_day, start_month, start_year = start_date.split('.')
                self.start_date = datetime(int(start_year), int(start_month), int(start_day))
            except:
                now = datetime.now()
                self.start_date = datetime(now.year - 1, 1, 1)
            
            # parse end date
            try:
                end_day, end_month, end_year = end_date.split('.')
                self.end_date = datetime(int(end_year), int(end_month), int(end_day))
            except:
                self.end_date = datetime.now()
            
            # update
            self._update_date_range_text()
            self._update_stats()
            self._update_chart()
            
            modal.dismiss()
            
            self.show_success_message("Фільтр застосовано")
            
        except Exception as e:
            self.show_error_message(f"Помилка фільтрації: {str(e)}")
    
    def go_to_transactions(self):
        """Navigate back to the transactions transactions screen."""
        self.switch_screen('transactions_screen', 'right')
    
    def show_menu(self):
        """Show application menu."""
        # modal
        popup = ModalView(
            size_hint=(0.7, 0.25),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )
        
        # content
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )
        
        with content.canvas.before:
            Color(rgba=get_primary_color())
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(10)])
        
        content.bind(size=self._update_rect, pos=self._update_rect)
        
        # title
        title_label = Label(
            text='Меню',
            font_size=sp(18),
            bold=True,
            color=get_text_primary_color(),
            size_hint_y=None,
            height=dp(40)
        )
        
        # buttons
        logout_btn = RoundedButton(
            text='Вийти з акаунту',
            size_hint_y=None,
            height=dp(45),
            bg_color='#D8F3EB',
            text_color=[0.04, 0.25, 0.21, 1]
        )
        
        exit_btn = RoundedButton(
            text='Вихід із програми',
            size_hint_y=None,
            height=dp(45),
            bg_color='#D8F3EB',
            text_color=[0.04, 0.25, 0.21, 1]
        )
        
        # bind button actions
        logout_btn.bind(on_press=lambda x: [popup.dismiss(), self.logout()])
        exit_btn.bind(on_press=lambda x: [popup.dismiss(), self.exit_app()])
        
        # add elements to content
        content.add_widget(title_label)
        content.add_widget(logout_btn)
        content.add_widget(exit_btn)
        
        popup.add_widget(content)
        
        popup.open()
    
    def logout(self):
        """Log out the current user."""
        from kivy.app import App
        app = App.get_running_app()
 
        if hasattr(app, 'auth_controller'):
            app.auth_controller.logout()

        self.switch_screen('first_screen', 'right')
    
    def exit_app(self):
        """Exit the application."""
        from kivy.app import App
        App.get_running_app().stop()
    
    def _update_rect(self, instance, value):
        """Update content rectangle when size or position changes."""
        if hasattr(self, 'content_rect'):
            self.content_rect.pos = instance.pos
            self.content_rect.size = instance.size
            
    def get_stats_display(self):
        """
        Get formatted statistics for display.
        
        Returns:
            Dictionary with formatted statistics values
        """
        avg_formatted = format_amount(self.avg_value, currency='UAH', show_sign=False)
        min_formatted = format_amount(self.min_value, currency='UAH', show_sign=False)
        max_formatted = format_amount(self.max_value, currency='UAH', show_sign=False)
        total_formatted = format_amount(self.total_value, currency='UAH', show_sign=False)

        count_formatted = str(int(self.count_value))
  
        top_category = self.top_category if hasattr(self, 'top_category') else 'Немає даних'
        
        return {
            'avg': avg_formatted,
            'min': min_formatted,
            'max': max_formatted,
            'total': total_formatted,
            'count': count_formatted,
            'top_category': top_category
        }