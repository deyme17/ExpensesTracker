from app.services.analytics.analytics_service import AnalyticsService
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes

class AnalyticsController:
    def __init__(self):
        self.analytics_service = AnalyticsService()

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
