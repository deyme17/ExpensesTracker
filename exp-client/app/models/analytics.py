from app.utils.language_mapper import LanguageMapper as LM
from datetime import datetime


class AnalyticsData:
    """
    Container for analytics data and statistics.
    """
    def __init__(self, stats, raw_transactions, transaction_type, start_date, end_date):
        self.stats = stats
        self.raw_transactions = raw_transactions
        self.transaction_type = transaction_type
        self.start_date = start_date
        self.end_date = end_date

    def get_avg_value(self) -> float:
        return self.stats["avg"]

    def get_min_value(self) -> float:
        return self.stats["min"]

    def get_max_value(self) -> float:
        return self.stats["max"]

    def get_total(self) -> float:
        return self.stats["total"]

    def get_count(self) -> float:
        return self.stats["count"]

    def get_top_category(self) -> str:
        return self.stats["top_category"]

    @staticmethod
    def empty(transaction_type: str, start_date: datetime, end_date: datetime) -> 'AnalyticsData':
        return AnalyticsData(
            stats={
                "avg": 0,
                "min": 0,
                "max": 0,
                "total": 0,
                "count": 0,
                "top_category": LM.message("no_data")
            },
            raw_transactions=[],
            transaction_type=transaction_type,
            start_date=start_date,
            end_date=end_date
        )