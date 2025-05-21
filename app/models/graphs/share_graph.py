from app.models.graphs.base_graph import BaseGraphWidget
from app.utils.language_mapper import LanguageMapper as LM


class ShareGraph(BaseGraphWidget):
    """
    Circular distribution chart by categories.
    """

    def fit(self, transactions):
        if not transactions:
            return []

        category_totals = {}
        for t in transactions:
            category = t.category or LM.message("unknown_category")
            category_totals[category] = category_totals.get(category, 0) + t.amount

        total = sum(category_totals.values()) or 1
        data = [
            (cat, round(value, 2), round(value / total * 100, 2))
            for cat, value in category_totals.items()
        ]
        data.sort(key=lambda x: x[1], reverse=True)
        return data