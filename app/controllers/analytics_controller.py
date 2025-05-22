from app.utils.language_mapper import LanguageMapper as LM
from datetime import datetime
from collections import defaultdict

class AnalyticsController:
    def __init__(self):
        pass

    def get_statistics(self, transactions):
        if not transactions:
            return {
                "avg": 0,
                "min": 0,
                "max": 0,
                "total": 0,
                "count": 0,
                "top_category": LM.message("no_data")
            }

        amounts = [abs(tx.amount) for tx in transactions]
        total = sum(amounts)
        count = len(amounts)
        avg = total / count if count else 0
        min_val = min(amounts)
        max_val = max(amounts)
        top_category = self._calc_top_category(transactions)

        return {
            "avg": round(avg, 2),
            "min": round(min_val, 2),
            "max": round(max_val, 2),
            "total": round(total, 2),
            "count": count,
            "top_category": top_category
        }

    def _calc_top_category(self, transactions):
        category_sums = defaultdict(float)
        for tx in transactions:
            category_sums[tx.category] += abs(tx.amount)
        top_category = max(category_sums.items(), key=lambda x: x[1])[0] if category_sums else "—"     
        return top_category  