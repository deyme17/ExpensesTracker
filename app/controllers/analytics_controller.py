from datetime import datetime, timedelta
from app.models.analytics import AnalyticsData


class AnalyticsController:
    def __init__(self, storage_service):
        """
        Initialize the analytics controller.
        
        Args:
            storage_service: Service for accessing transaction data
        """
        self.storage_service = storage_service
    
    def get_analytics_data(self, transaction_type='Витрати', start_date=None, end_date=None):
        """
        Get analytics data for the specified criteria.
        
        Args:
            transaction_type: 'Витрати' or 'Доходи'
            start_date: Start date for analysis
            end_date: End date for analysis
                
        Returns:
            AnalyticsData object with statistics and chart data
        """
        if not end_date:
            end_date = datetime.now()
        if not start_date:
            start_date = datetime(end_date.year - 1, 1, 1)
    
        is_income = transaction_type == 'Доходи'

        transactions = self._get_filtered_transactions(is_income, start_date, end_date)

        stats = self._calculate_statistics(transactions)
        
        # prepare chart data
        bar_chart_data = self._prepare_bar_chart_data(transactions, start_date, end_date)
        pie_chart_data = self._prepare_pie_chart_data(transactions)
        line_chart_data = self._prepare_line_chart_data(transactions, start_date, end_date)
        
        # analytics data object
        analytics_data = AnalyticsData(
            stats=stats,
            bar_chart_data=bar_chart_data,
            pie_chart_data=pie_chart_data,
            line_chart_data=line_chart_data,
            transaction_type=transaction_type,
            start_date=start_date,
            end_date=end_date
        )
        
        return analytics_data
    
    def _get_filtered_transactions(self, is_income, start_date, end_date):
        """
        Get transactions filtered by type and date range.
        
        Args:
            is_income: If True, get income transactions; if False, get expense transactions
            start_date: Start date for filtering
            end_date: End date for filtering
            
        Returns:
            List of Transaction objects
        """
        all_transactions = self.storage_service.get_transactions()
        
        filtered_transactions = [
            t for t in all_transactions
            if t.is_income == is_income
            and start_date <= t.date <= end_date
        ]
        
        return filtered_transactions
    
    def _calculate_statistics(self, transactions):
        """
        Calculate basic statistics for a list of transactions.
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            Dictionary with statistics
        """
        if not transactions:
            return {
                'avg_value': 0,
                'min_value': 0,
                'max_value': 0,
                'total': 0,
                'count': 0,
                'top_category': 'Немає даних'
            }
        
        try:
            amounts = [abs(t.amount) for t in transactions]
            
            avg_value = sum(amounts) / len(amounts) if amounts else 0
            min_value = min(amounts) if amounts else 0
            max_value = max(amounts) if amounts else 0
            total = sum(amounts) if amounts else 0
            count = len(amounts)

            category_totals = {}
            for t in transactions:
                category = t.category
                amount = abs(t.amount)
                
                if category in category_totals:
                    category_totals[category] += amount
                else:
                    category_totals[category] = amount
            
            top_category = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else 'Немає даних'
            
            stats = {
                'avg_value': avg_value,
                'min_value': min_value,
                'max_value': max_value,
                'total': total,
                'count': count,
                'top_category': top_category
            }
            
            return stats
            
        except Exception as e:
            print(f"ERROR: Помилка при обчисленні статистики: {str(e)}")
            return {
                'avg_value': 0,
                'min_value': 0,
                'max_value': 0,
                'total': 0,
                'count': 0,
                'top_category': 'Помилка обчислення'
            }
    
    def _prepare_bar_chart_data(self, transactions, start_date, end_date): # TODO Тут треба розподіл величин витрат/доходів а не місяців
        """
        Prepare data for the bar chart (amount distribution).
        
        Args:
            transactions: List of Transaction objects
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            List of dictionaries with chart data
        """
        current_date = start_date.replace(day=1)
        end_month = end_date.replace(day=1)
        
        monthly_data = {}
        
        while current_date <= end_month:
            month_name = current_date.strftime('%b')
            month_key = (current_date.year, current_date.month)
            monthly_data[month_key] = {
                'name': month_name,
                'value': 0,
                'month': current_date.month,
                'year': current_date.year
            }
            
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        # aggregate transaction amounts by month
        for transaction in transactions:
            month_key = (transaction.date.year, transaction.date.month)
            if month_key in monthly_data:
                monthly_data[month_key]['value'] += abs(transaction.amount)
        
        # convert to list and sort by date
        chart_data = list(monthly_data.values())
        chart_data.sort(key=lambda x: (x['year'], x['month']))
        
        return chart_data
    
    def _prepare_pie_chart_data(self, transactions):
        """
        Prepare data for the pie chart (category distribution).
        
        Args:
            transactions: List of Transaction objects
            
        Returns:
            List of dictionaries with chart data
        """
        category_totals = {}
        
        # aggregate transaction amounts by category
        for transaction in transactions:
            category = transaction.category
            amount = abs(transaction.amount)
            
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        
        # convert to list
        chart_data = [
            {'name': category, 'value': amount}
            for category, amount in category_totals.items()
        ]
        
        # sort by value
        chart_data.sort(key=lambda x: x['value'], reverse=True)
        
        return chart_data
    
    def _prepare_line_chart_data(self, transactions, start_date, end_date):
        """
        Prepare data for the line chart (daily trend).
        
        Args:
            transactions: List of Transaction objects
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            List of dictionaries with chart data
        """
        date_range = (end_date - start_date).days
        use_weekly = date_range > 30
        
        if use_weekly:
            return self._prepare_weekly_line_data(transactions, start_date, end_date)
        else:
            return self._prepare_daily_line_data(transactions, start_date, end_date)
    
    def _prepare_daily_line_data(self, transactions, start_date, end_date):
        """Prepare daily line chart data."""
        current_date = start_date
        daily_data = {}
        
        while current_date <= end_date:
            date_str = current_date.strftime('%d.%m')
            daily_data[current_date.date()] = {
                'name': date_str,
                'value': 0,
                'date': current_date.date()
            }
            
            current_date += timedelta(days=1)
        
        # aggregate transaction amounts by day
        for transaction in transactions:
            if transaction.date.date() in daily_data:
                daily_data[transaction.date.date()]['value'] += abs(transaction.amount)
        
        # convert to list and sort by date
        chart_data = list(daily_data.values())
        chart_data.sort(key=lambda x: x['date'])
        
        for item in chart_data:
            del item['date']
        
        return chart_data
    
    def _prepare_weekly_line_data(self, transactions, start_date, end_date):
        """Prepare weekly line chart data."""
        weekly_data = {}
        
        def get_week_key(date):
            # ISO week number with year
            year = date.isocalendar()[0]
            week = date.isocalendar()[1]
            return (year, week)
        
        # unique weeks in the date range
        current_date = start_date
        while current_date <= end_date:
            week_key = get_week_key(current_date)
            if week_key not in weekly_data:
                week_name = f"W{week_key[1]}"
                weekly_data[week_key] = {
                    'name': week_name,
                    'value': 0,
                    'year': week_key[0],
                    'week': week_key[1]
                }
            
            current_date += timedelta(days=1)
        
        # aggregate transaction amounts by week
        for transaction in transactions:
            week_key = get_week_key(transaction.date)
            if week_key in weekly_data:
                weekly_data[week_key]['value'] += abs(transaction.amount)
        
        # Convert to list and sort by date
        chart_data = list(weekly_data.values())
        chart_data.sort(key=lambda x: (x['year'], x['week']))
        
        return chart_data