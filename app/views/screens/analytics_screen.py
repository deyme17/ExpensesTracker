from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from datetime import datetime

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.analytics_widgets.analytics_filter_popup import AnalyticsFilterPopup
from app.views.widgets.analytics_widgets.graph_section import GraphSection
from app.views.widgets.analytics_widgets.stats_section import StatsSection

from app.utils.language_mapper import LanguageMapper as LM
from app.utils.constants import CHART_TYPE_HISTOGRAM, EXPENSE
from app.utils.state_savers import AnalyticsFilterState


Builder.load_file("kv/analytics_screen.kv")


class AnalyticsScreen(BaseScreen):
    """
    Screen for displaying financial analytics and visualizations.
    Args:
        transaction_controller: Handles transaction data
        analytics_controller: Handles statistics logic
        graph_factory: Responsible for building graphs (renderer + strategy)
        local_storage: Persistent storage handler
    """
    current_chart_type = StringProperty(CHART_TYPE_HISTOGRAM)
    current_type = StringProperty(EXPENSE)
    translated_type = StringProperty("")
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)

    def __init__(self, transaction_controller, analytics_controller, graph_factory, local_storage, **kwargs):
        super().__init__(**kwargs)
        # data range
        now = datetime.now()
        self.start_date = datetime(now.year - 1, 1, 1)
        self.end_date = now

        # controllers
        self.transaction_controller = transaction_controller
        self.analytics_controller = analytics_controller
        self.graph_factory = graph_factory
        self.local_storage = local_storage

        # state
        self._filter_state = AnalyticsFilterState()
        self.selected_account_id = self.local_storage.get_active_account_id()

        # sections
        self.stats_section = None
        self.graph_section = None

        self.data = None

    def on_enter(self):
        super().on_enter()
        self._load_analytics_data()

    def _load_analytics_data(self, *args):
        """
        Loads transactions, applies filters, computes statistics and updates UI sections.
        """
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
        else:
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
        """
        Updates graph and stats sections with current analytics data.
        """
        if not self.graph_section:
            self.graph_section = GraphSection(graph_factory=self.graph_factory)
            graph_box = self.ids["graph_box"]
            graph_box.clear_widgets()
            graph_box.add_widget(self.graph_section)

        self.graph_section.update_graph(
            transactions=self.data.raw_transactions,
            chart_type=self.current_chart_type
        )

        if not self.stats_section:
            self.stats_section = StatsSection()
            stats_box = self.ids["stats_box"]
            stats_box.clear_widgets()
            stats_box.add_widget(self.stats_section)

        self.stats_section.update_stats(
            self.data.stats,
            transaction_type=self.current_type
        )

        self.translated_type = LM.transaction_type(self.current_type)

    def change_chart_type(self, chart_type: str):
        """
        Handles chart type switching (e.g., from histogram to pie).
        """
        if self.current_chart_type == chart_type:
            return

        self.current_chart_type = chart_type
        if self.graph_section and self.data:
            self.graph_section.update_graph(
                transactions=self.data.raw_transactions,
                chart_type=self.current_chart_type
            )

    def refresh_analytics(self):
        """
        Reloads transactions and updates all sections.
        """
        self.selected_account_id = self.local_storage.get_active_account_id()
        self._load_analytics_data()
        self._update_sections()

# filter
    def show_filter(self):
        """
        Opens the filter popup to apply transaction filters.
        """
        popup = AnalyticsFilterPopup(
            filter_state=self._filter_state,
            on_apply=self._apply_filter,
            on_reset=self._reset_filter
        )
        popup.open()

    def _apply_filter(self, current_type, start_date, end_date):
        """
        Called when user applies filters from popup.
        """
        self._filter_state.update(
            current_type=current_type,
            start_date=start_date,
            end_date=end_date
        )
        self.current_type = current_type
        self.start_date = start_date
        self.end_date = end_date
        self.translated_type = LM.transaction_type(current_type)

        self._load_analytics_data()
        self._update_sections()
        self.show_success_message(LM.message("filter_applied"))

    def _reset_filter(self):
        """
        Resets filter state.
        """
        self._filter_state.reset()
        
# navig
    def go_to_transactions(self):
        """
        Navigates back to transactions screen.
        """
        if self.manager:
            self.manager.transition.direction = "right"
            self.manager.current = "transactions_screen"
