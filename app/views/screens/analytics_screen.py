from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.analytics_widgets.analytics_filter_popup import AnalyticsFilterPopup
from app.views.widgets.analytics_widgets.graph_section import GraphSection
from app.views.widgets.analytics_widgets.stats_section import StatsSection
from app.views.widgets.popups.menu_popup import MenuPopup
from app.utils.constants import TRANSACTION_TYPE_EXPENSE, CHART_TYPE_HISTOGRAM
from app.utils.formatters import format_amount, format_date_range
from kivy.app import App

Builder.load_file('kv/analytics_screen.kv')

class AnalyticsScreen(BaseScreen):
    current_chart_type = StringProperty(CHART_TYPE_HISTOGRAM)
    current_type = StringProperty(TRANSACTION_TYPE_EXPENSE)
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)
    date_range_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'analytics_screen'
        now = datetime.now()
        self.start_date = datetime(now.year - 1, 1, 1)
        self.end_date = now

        self.stats_section = None
        self.graph_section = None

        app = App.get_running_app()
        self.transaction_controller = app.transaction_controller
        self.analytics_controller = app.analytics_controller

    def on_enter(self):
        super().on_enter()
        Clock.schedule_once(self._load_analytics_data, 0.1)

    def _load_analytics_data(self, dt):
        transactions = self.transaction_controller.filter_transactions(
            is_income=(self.current_type != TRANSACTION_TYPE_EXPENSE),
            start_date=self.start_date,
            end_date=self.end_date
        )

        stats = self.analytics_controller.get_statistics(transactions)

        if self.stats_section is None:
            self.stats_section = StatsSection()
            self.ids.stats_box.clear_widgets()
            self.ids.stats_box.add_widget(self.stats_section)

        stats_dict = {
            'avg': format_amount(stats['avg_value']),
            'min': format_amount(stats['min_value']),
            'max': format_amount(stats['max_value']),
            'total': format_amount(stats['total']),
            'count': str(stats['count']),
            'top_category': stats['top_category'],
        }

        if not self.stats_section:
            self.stats_section = StatsSection()
            self.ids.stats_box.clear_widgets()
            self.ids.stats_box.add_widget(self.stats_section)

        self.stats_section.update_stats(stats_dict)

    def change_chart_type(self, chart_type):
        if self.current_chart_type == chart_type:
            return
        
        self.current_chart_type = chart_type

        if self.graph_section:
            self.graph_section.chart_type = chart_type


    def show_filter(self):
        popup = AnalyticsFilterPopup(
            current_type=self.current_type,
            start_date=self.start_date,
            end_date=self.end_date
        )
        popup.on_apply_callback = self._apply_filter
        popup.open()

    def _apply_filter(self, transaction_type, start_date, end_date):
        self.current_type = transaction_type
        self.start_date = start_date
        self.end_date = end_date
        self._load_analytics_data(0)

    def go_to_transactions(self):
        if self.manager:
            self.manager.transition.direction = 'right'
            self.manager.current = 'transactions_screen'
