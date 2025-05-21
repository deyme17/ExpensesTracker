from app.services.graph_factory import GraphFactory
from app.utils.language_mapper import LanguageMapper

class AnalyticsController:
    def __init__(self):
        self.graph_factory = GraphFactory()

    def get_statistics(self, transactions):
        if not transactions:
            return {
                'avg_value': 0,
                'min_value': 0,
                'max_value': 0,
                'total': 0,
                'count': 0,
                'top_category': LanguageMapper.message("no_data")
            }

        amounts = [abs(t.amount) for t in transactions]
        total = sum(amounts)
        category_totals = {}
        for t in transactions:
            category_totals[t.category] = category_totals.get(t.category, 0) + abs(t.amount)

        return {
            'avg_value': total / len(transactions),
            'min_value': min(amounts),
            'max_value': max(amounts),
            'total': total,
            'count': len(transactions),
            'top_category': max(category_totals.items(), key=lambda x: x[1])[0]
        }

    def get_chart(self, chart_type, transactions, **kwargs):
        graph = self.graph_factory.create_graph(
            chart_type=chart_type,
            transactions=transactions,
            **kwargs
        )
        return graph.prepare_chart_data()
