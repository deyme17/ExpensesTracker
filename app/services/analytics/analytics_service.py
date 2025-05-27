from collections import defaultdict
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
import hashlib

class AnalyticsService:
    def __init__(self):
        self._last_hash = None
        self._last_result = None

    def get_statistics(self, transactions):
        current_hash = self._compute_hash(transactions)

        if current_hash == self._last_hash:
            return self._last_result, None

        try:
            if not transactions:
                result = {
                    "avg": 0,
                    "min": 0,
                    "max": 0,
                    "total": 0,
                    "count": 0,
                    "top_category": LM.message("no_data")
                }
            else:
                amounts = [abs(tx.amount) for tx in transactions]
                total = sum(amounts)
                count = len(amounts)
                avg = total / count if count else 0
                min_val = min(amounts)
                max_val = max(amounts)
                top_category = self._calc_top_category(transactions)

                result = {
                    "avg": round(avg, 2),
                    "min": round(min_val, 2),
                    "max": round(max_val, 2),
                    "total": round(total, 2),
                    "count": count,
                    "top_category": LM.category(top_category)
                }

            self._last_hash = current_hash
            self._last_result = result
            return result, None
        except Exception:
            return {}, ErrorCodes.UNKNOWN_ERROR

    def _calc_top_category(self, transactions):
        from kivy.app import App
        category_service = App.get_running_app().category_service

        category_sums = defaultdict(float)
        try:
            for tx in transactions:
                name = category_service.get_category_name_by_mcc(tx.mcc_code)
                category_sums[name] += abs(tx.amount)
            return max(category_sums.items(), key=lambda x: x[1])[0] if category_sums else "—"
        except Exception:
            return "—"

    def _compute_hash(self, transactions):
        if not transactions:
            return None
        hasher = hashlib.md5()
        for tx in transactions:
            s = f"{tx.transaction_id}-{tx.amount}-{tx.date.isoformat()}"
            hasher.update(s.encode('utf-8'))
        return hasher.hexdigest()