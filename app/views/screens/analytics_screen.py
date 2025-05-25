from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime

from app.views.screens.base_screen import BaseScreen
from app.models.analytics import AnalyticsData
from app.views.widgets.analytics_widgets.analytics_filter_popup import AnalyticsFilterPopup
from app.views.widgets.analytics_widgets.graph_section import GraphSection
from app.views.widgets.analytics_widgets.stats_section import StatsSection
from app.utils.constants import CHART_TYPE_HISTOGRAM
from app.utils.language_mapper import LanguageMapper as LM
from app.services.local_storage import LocalStorageService

Builder.load_file("kv/analytics_screen.kv")

class AnalyticsScreen(BaseScreen):
    current_chart_type = StringProperty(CHART_TYPE_HISTOGRAM)
    current_type = StringProperty("expense")
    translated_type = StringProperty("")
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "analytics_screen"

        now = datetime.now()
        self.start_date = datetime(now.year - 1, 1, 1)
        self.end_date = now

        self.stats_section = None
        self.graph_section = None

        from kivy.app import App
        app = App.get_running_app()
        self.transaction_controller = app.transaction_controller
        self.analytics_controller = app.analytics_controller
        self.selected_account_id = app.account_service.storage_service.get_active_account_id()

        self.storage = LocalStorageService()
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
            self.data = AnalyticsData.empty()
            self._update_sections()
            return

        stats = self.analytics_controller.get_statistics(transactions)

        self.data = AnalyticsData(
            stats=stats,
            raw_transactions=transactions,
            transaction_type=self.current_type,
            start_date=self.start_date,
            end_date=self.end_date
        )
        self._update_sections()

    def _update_sections(self):
        if not self.graph_section:
            self.graph_section = GraphSection(chart_type=self.current_chart_type)
            self.ids.graph_box.clear_widgets()
            self.ids.graph_box.add_widget(self.graph_section)

        self.graph_section.update_graph(self.data.raw_transactions)

        if not self.stats_section:
            self.stats_section = StatsSection()
            self.ids.stats_box.clear_widgets()
            self.ids.stats_box.add_widget(self.stats_section)

        self.stats_section.update_stats(self.data.stats, transaction_type=self.current_type)
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
        self._load_analytics_data(0)
        self.show_success_message(LM.message("filter_applied"))

    def change_chart_type(self, chart_type):
        if self.current_chart_type == chart_type:
            return
        self.current_chart_type = chart_type
        if self.graph_section:
            self.graph_section.chart_type = chart_type
            self.graph_section.update_graph(self.data.raw_transactions)

    def go_to_transactions(self):
        if self.manager:
            self.manager.transition.direction = "right"
            self.manager.current = "transactions_screen"