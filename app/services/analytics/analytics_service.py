from collections import defaultdict
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.error_codes import ErrorCodes
import hashlib

class AnalyticsService:
    """
    Provides transaction statistics and analytics with caching support.
    Args:
        category_service: Provides MCC code lookups and category management.
    """
    def __init__(self, category_service):
        self.category_service = category_service
        self._last_hash = None
        self._last_result = None

    def get_statistics(self, transactions):
        """
        Calculates key statistics for given transactions.
        Args:
            transactions: List of Transaction objects to analyze
        Returns:
            Tuple: (statistics_dict, error_message)
            
            statistics_dict contains:
            - avg: Average transaction amount
            - min: Minimum amount
            - max: Maximum amount  
            - total: Sum of amounts
            - count: Number of transactions
            - top_category: Most frequent category by amount
        """
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
        """
        Calculates the top spending category by total amount.
        Args:
            transactions: List of Transaction objects
        Returns:
            str: Name of top category or "—" if undetermined
        """
        category_sums = defaultdict(float)
        try:
            for tx in transactions:
                name = self.category_service.get_category_name_by_mcc(tx.mcc_code)
                category_sums[name] += abs(tx.amount)
            return max(category_sums.items(), key=lambda x: x[1])[0] if category_sums else "—"
        except Exception:
            return "—"

    def _compute_hash(self, transactions):
        """
        Generates MD5 hash of transactions for change detection.
        Args:
            transactions: List of Transaction objects
        Returns:
            str: Hex digest of transactions fingerprint or None if empty
        """
        if not transactions:
            return None
        hasher = hashlib.md5()
        for tx in transactions:
            s = f"{tx.transaction_id}-{tx.amount}-{tx.date.isoformat()}"
            hasher.update(s.encode('utf-8'))
        return hasher.hexdigest()