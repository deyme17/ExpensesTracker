from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
from app.models.analytics import AnalyticsData

from datetime import datetime


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

    def get_statistics(self, transactions: list) -> tuple[None|dict, None|str]:
        try:
            result, error = self.analytics_service.get_statistics(transactions)
            if error:
                return None, LM.server_error(error)
            return result, None
        
        except Exception:
            import traceback
            traceback.print_exc()
            return None, LM.server_error(ErrorCodes.UNKNOWN_ERROR)
        
    def get_analytics_data(self, transactions: list, transaction_type: str, 
                           start_date: datetime, end_date: datetime) -> tuple[AnalyticsData|None, None|str]:
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
    
    def get_empty_analytics(self, transaction_type: str, start_date: datetime, end_date: datetime) -> AnalyticsData:
        return AnalyticsData.empty(transaction_type, start_date, end_date)