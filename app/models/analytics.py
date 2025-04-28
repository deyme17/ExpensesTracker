from app.utils.constants import CHART_TYPE_HISTOGRAM, CHART_TYPE_LINE, CHART_TYPE_PIE

class AnalyticsData:
    def __init__(self, stats, bar_chart_data, pie_chart_data, line_chart_data,
                transaction_type, start_date, end_date):
        """
        Initialize an AnalyticsData instance.
        
        Args:
            stats (dict): Statistical data (min, max, avg, etc.)
            bar_chart_data (list): Data for bar chart (monthly distribution)
            pie_chart_data (list): Data for pie chart (category distribution)
            line_chart_data (list): Data for line chart (daily/weekly trend)
            transaction_type (str): 'Витрати' or 'Доходи'
            start_date (datetime): Start date of the analysis period
            end_date (datetime): End date of the analysis period
        """
        self.stats = stats
        self.bar_chart_data = bar_chart_data
        self.pie_chart_data = pie_chart_data
        self.line_chart_data = line_chart_data
        self.transaction_type = transaction_type
        self.start_date = start_date
        self.end_date = end_date
    
    def get_avg_value(self):
        """Get the average value of transactions"""
        return self.stats.get('avg_value', 0)

    def get_min_value(self):
        """Get the minimum value of transactions"""
        return self.stats.get('min_value', 0)

    def get_max_value(self):
        """Get the maximum value of transactions"""
        return self.stats.get('max_value', 0)

    def get_total(self):
        """Get the total amount of transactions"""
        return self.stats.get('total', 0)

    def get_count(self):
        """Get the number of transactions"""
        return self.stats.get('count', 0)

    def get_top_category(self):
        """Get the top category by amount"""
        return self.stats.get('top_category', 'No data')

    def get_chart_data(self, chart_type):
        """
        Get data for a specific chart type.

        Args:
            chart_type: Chart type ('histogram', 'pie', 'line')

        Returns:
            Data for the given chart type
        """
        if chart_type == CHART_TYPE_HISTOGRAM:
            return self.bar_chart_data
        elif chart_type == CHART_TYPE_PIE:
            return self.pie_chart_data
        elif chart_type == CHART_TYPE_LINE:
            return self.line_chart_data
        else:
            return []