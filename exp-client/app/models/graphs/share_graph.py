from collections import defaultdict
from kivy.properties import ListProperty
from app.models.graphs.base_graph import BaseGraph
from app.utils.constants import SHARE_NUM
from app.utils.language_mapper import LanguageMapper


class ShareGraph(BaseGraph):
    """
    Pie chart model of transaction share by category.
    """
    transactions = ListProperty([])

    def __init__(self, category_service, **kwargs):
        super().__init__(**kwargs)
        self.category_service = category_service

    def fit(self, transactions):
        totals = defaultdict(float)
        
        for tx in transactions:
            raw_name = self.category_service.get_category_name_by_mcc(tx.mcc_code)
            translated_name = LanguageMapper.category(raw_name)
            totals[translated_name] += abs(tx.amount)

        items = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:SHARE_NUM]

        if not items:
            return [], []
        
        labels, values = zip(*items)
        return labels, values