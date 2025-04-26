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
        """Отримати середнє значення транзакцій"""
        return self.stats.get('avg_value', 0)
    
    def get_min_value(self):
        """Отримати мінімальне значення транзакцій"""
        return self.stats.get('min_value', 0)
    
    def get_max_value(self):
        """Отримати максимальне значення транзакцій"""
        return self.stats.get('max_value', 0)
    
    def get_total(self):
        """Отримати загальну суму транзакцій"""
        return self.stats.get('total', 0)
    
    def get_count(self):
        """Отримати кількість транзакцій"""
        return self.stats.get('count', 0)
    
    def get_top_category(self):
        """Отримати топ-категорію за сумою"""
        return self.stats.get('top_category', 'Немає даних')
    
    def get_chart_data(self, chart_type):
        """
        Отримати дані для конкретного типу діаграми.
        
        Args:
            chart_type: Тип діаграми ('histogram', 'pie', 'line')
            
        Returns:
            Дані для вказаного типу діаграми
        """
        if chart_type == 'histogram':
            return self.bar_chart_data
        elif chart_type == 'pie':
            return self.pie_chart_data
        elif chart_type == 'line':
            return self.line_chart_data
        else:
            return []