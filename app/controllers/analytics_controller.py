from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
from app.services.analytics.graph_factory import GraphFactory
from app.models.analytics import AnalyticsData

class AnalyticsController:
    """
    Handles business logic for analytics operations including statistics and graph generation.
    Args:
        analytics_service: Service layer for core analytics calculations and data processing.
    """

    def __init__(self, analytics_service):
        self.analytics_service = analytics_service
        # cache
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
        
    def get_analytics_data(self, transactions, transaction_type, start_date, end_date):
        stats, error = self.get_statistics(transactions)
        if error:
            return None, error

        data = AnalyticsData(
            stats=stats,
            raw_transactions=transactions,
            transaction_type=transaction_type,
            start_date=start_date,
            end_date=end_date
        )
        return data, None
    
    def get_empty_analytics(self, transaction_type, start_date, end_date):
        return AnalyticsData.empty(transaction_type, start_date, end_date)

    def create_graph(self, chart_type, transactions, transaction_type, category=None): #???
        try:
            key = (chart_type, transaction_type, category, len(transactions))
            
            if self._last_graph_key == key:
                return self._last_graph

            # Factory
            widget = GraphFactory.create_graph(
                chart_type=chart_type,
                controller=self,
                transaction_type=transaction_type,
                transactions=transactions,
                category=category
            )

            # Update cache
            self._last_graph_key = key
            self._last_graph = widget
            return widget
        
        except Exception:
            import traceback
            traceback.print_exc()
            return None