from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from app.utils.constants import CHART_TYPE_HISTOGRAM, EXPENSE
from app.views.widgets.analytics_widgets.analytics_filter_popup import AnalyticsFilterPopup #???
from app.views.widgets.analytics_widgets.graph_section import GraphSection #???

from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.analytics_widgets.stats_section import StatsSection #???
from app.utils.language_mapper import LanguageMapper as LM

Builder.load_file("kv/analytics_screen.kv")


class AnalyticsScreen(BaseScreen):
    current_chart_type = StringProperty(CHART_TYPE_HISTOGRAM)
    current_type = StringProperty(EXPENSE)
    translated_type = StringProperty("")
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)

    def __init__(self, transaction_controller, analytics_controller, local_storage, **kwargs):
        super().__init__(**kwargs)
        # period
        now = datetime.now()
        self.start_date = datetime(now.year - 1, 1, 1)
        self.end_date = now

        # components
        self.stats_section = None
        self.graph_section = None

        # controllers
        self.transaction_controller = transaction_controller
        self.analytics_controller=analytics_controller
        
        # data
        self.storage = local_storage
        self.selected_account_id = self.storage.get_active_account_id()

    def on_enter(self):
        super().on_enter()
        self._load_analytics_data()

    def _load_analytics_data(self, *args):
        transactions = self.transaction_controller.filter_transactions(
            min_amount=0,
            max_amount=1e9,
            start_date=self.start_date,
            end_date=self.end_date,
            type=self.current_type,
            account_id=self.selected_account_id
        )

        if not transactions:
            self.data = self.analytics_controller.get_empty_analytics(
                transaction_type=self.current_type,
                start_date=self.start_date,
                end_date=self.end_date
            )
            self._update_sections()
            return

        data, error = self.analytics_controller.get_analytics_data(
            transactions=transactions,
            transaction_type=self.current_type,
            start_date=self.start_date,
            end_date=self.end_date
        )
        if error:
            self.show_error_message(error)
            return
        self.data = data

        self._update_sections()

    def _update_sections(self):
        if not self.graph_section:
            self.graph_section = GraphSection(chart_type=self.current_chart_type)
            container = self.ids['graph_box']
            container.clear_widgets()
            container.add_widget(self.graph_section)

        self.graph_section.update_graph(
            transactions=self.data.raw_transactions,
            chart_type=self.current_chart_type
        )

        if not self.stats_section:
            self.stats_section = StatsSection()
            self.ids['stats_box'].clear_widgets()
            self.ids['stats_box'].add_widget(self.stats_section)

        self.stats_section.update_stats(
            self.data.stats,
            transaction_type=self.current_type
        )
        self.translated_type = LM.transaction_type(self.current_type)

    def show_filter(self):
        popup = AnalyticsFilterPopup(
            current_type=self.current_type,
            start_date=self.start_date,
            end_date=self.end_date
        )
        popup.on_apply = self._apply_filter
        popup.open()

    def _apply_filter(self, transaction_type, start_date, end_date):
        self.current_type = transaction_type
        self.translated_type = LM.transaction_type(transaction_type)
        self.start_date = start_date
        self.end_date = end_date
        Clock.schedule_once(lambda dt: self._update_chart_type(), 0)
        self.show_success_message(LM.message("filter_applied"))
        self._load_analytics_data()
        self._update_sections()

    def _update_chart_type(self):
        if self.graph_section:
            self.graph_section.update_graph(
                transactions=self.data.raw_transactions,
                chart_type=self.current_chart_type
            )

    def change_chart_type(self, chart_type):
        if self.current_chart_type == chart_type:
            return
        self.current_chart_type = chart_type
        if self.graph_section:
            self.graph_section.update_graph(
                transactions=self.data.raw_transactions,
                chart_type=self.current_chart_type
            )

    def refresh_analytics(self):
        self.selected_account_id = self.storage.get_active_account_id()
        self._load_analytics_data()
        self._update_sections()
        
    def go_to_transactions(self):
        if self.manager:
            self.manager.transition.direction = "right"
            self.manager.current = "transactions_screen"