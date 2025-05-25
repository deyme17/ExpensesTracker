from datetime import datetime
from app.utils.constants import SHORT_MONTHS, LONG_MONTHS
from app.utils.language_mapper import LanguageMapper as LM

def format_amount(amount, currency, show_sign=True):
    """
    Format a monetary amount.
    
    Args:
        amount (float): Amount to format
        currency (str): Currency code
        show_sign (bool): Whether to show + or - sign
        
    Returns:
        str: Formatted amount string
    """
    is_negative = amount < 0
    abs_amount = abs(amount)
    
    formatted = f"{abs_amount:,.2f}"
    
    if show_sign:
        sign = "-" if is_negative else "+"
        formatted = f"{sign}{formatted}"
    elif is_negative:
        formatted = f"-{formatted}"
    
    formatted = f"{formatted} ({currency})"
    
    return formatted

def format_date(date, format_str="%d.%m.%Y"):
    """
    Format a date.
    
    Args:
        date (datetime): Date to format
        format_str (str): Format string
        
    Returns:
        str: Formatted date string
    """
    if not date:
        return ""
    
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return date
    
    return date.strftime(format_str)

def format_date_range(start_date, end_date, format_str="%d.%m.%Y"):
    """
    Format a date range.
    
    Args:
        start_date (datetime): Start date
        end_date (datetime): End date
        format_str (str): Format string
        
    Returns:
        str: Formatted date range string
    """
    start_str = format_date(start_date, format_str)
    end_str = format_date(end_date, format_str)
    
    return f"{start_str} - {end_str}"

def get_month_name(month_number, short=True):
    """
    Get month name from month number.
    
    Args:
        month_number (int): Month number (1-12)
        short (bool): Whether to use abbreviated month name
        
    Returns:
        str: Month name
    """
    if not 1 <= month_number <= 12:
        return ""

    if short:
        month_en = SHORT_MONTHS[month_number - 1]
    else:
        month_en = LONG_MONTHS[month_number - 1]

    return LM.month_name(month_en, short=short)

def format_percent(value, decimal_places=1):
    """
    Format a value as a percentage.
    
    Args:
        value (float): Value to format
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted percentage string
    """
    format_str = f"{{:.{decimal_places}f}}%"
    return format_str.format(value * 100)
