from app.models.graphs.distribution_graph import DistributionGraph
from app.models.graphs.dynamics_graph import DynamicsGraph
from app.models.graphs.share_graph import ShareGraph


class GraphFactory:
    """
    Factory for creating and configuring different types of financial graphs.
    Implements the Strategy pattern to select appropriate graph types based on renderer configuration.
    Args: 
        category_service: Service for category data operations (is used in ShareGraph)
    """
    def __init__(self, category_service):
        self._strategies_by_key = {
            "distribution": lambda: DistributionGraph(),
            "line": lambda: DynamicsGraph(),
            "share": lambda: ShareGraph(category_service)
        }

    def create_graph(self, renderer, transactions):
        """
        Creates and configures a graph visualization.
        Args:
            renderer: Graph renderer with 'graph_key' attribute
            transactions: Transaction data to visualize
        Returns:
            Renderer instance with rendered data
        """
        graph_key = getattr(renderer, "graph_key", None)
        if graph_key is None or graph_key not in self._strategies_by_key:
            raise ValueError(f"No strategy found for renderer with key: {graph_key}")

        strategy_factory = self._strategies_by_key[graph_key]
        strategy = strategy_factory()

        x, y = strategy.fit(transactions)
        renderer._render(x, y)
        return renderer