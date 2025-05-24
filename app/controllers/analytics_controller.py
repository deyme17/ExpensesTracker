from app.services.analytics.analytics_service import AnalyticsService

class AnalyticsController:
    def __init__(self):
        self.analytics_service = AnalyticsService()

    def get_statistics(self, transactions):
        return self.analytics_service.get_statistics(transactions)
