from app.services.analytics.analytics_service import AnalyticsService
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
from app.services.analytics.graph_factory import GraphFactory

class AnalyticsController:
    def __init__(self):
        self.analytics_service = AnalyticsService()
        self._last_graph_key = None
        self._last_graph = None

    def get_statistics(self, transactions):
        try:
            result, error = self.analytics_service.get_statistics(transactions)
            if error:
                return None, LM.server_error(error)
            return result, None
        except Exception:
            import traceback
            traceback.print_exc()
            return None, LM.server_error(ErrorCodes.UNKNOWN_ERROR)

    def create_graph(self, chart_type, transactions, transaction_type, category=None):
        try:
            key = (chart_type, transaction_type, category, len(transactions))
            if self._last_graph_key == key:
                return self._last_graph

            widget = GraphFactory.create_graph(
                chart_type=chart_type,
                controller=self,
                transaction_type=transaction_type,
                transactions=transactions,
                category=category
            )

            self._last_graph_key = key
            self._last_graph = widget
            return widget
        except Exception:
            import traceback
            traceback.print_exc()
            return None
