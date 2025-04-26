import re
from datetime import datetime

def validate_email(email):
    """
    Validate an email address.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if the email is valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """
    Validate a password.
    
    Args:
        password (str): Password to validate
        
    Returns:
        bool: True if the password is valid, False otherwise
    """
    if not password:
        return False
    
    # Password must be at least 6 characters   # TODO
    return len(password) >= 6

def validate_monobank_token(token):
    """
    Validate a Monobank API token.
    
    Args:
        token (str): Monobank API token to validate
        
    Returns:
        bool: True if the token has the correct format, False otherwise
    """
    if not token:
        return False
    
    # Monobank token is a 32-character alphanumeric string  # TODO
    pattern = r'^[a-zA-Z0-9]{32}$'
    return bool(re.match(pattern, token))

def validate_amount(amount_str):
    """
    Validate a monetary amount string.
    
    Args:
        amount_str (str): Amount string to validate
        
    Returns:
        (bool, float): (is_valid, parsed_amount)
    """
    if not amount_str:
        return False, 0.0
    
    try:
        amount_str = amount_str.replace(',', '.')
        
        amount_str = amount_str.strip()
        amount_str = re.sub(r'[^\d.-]', '', amount_str)
        
        amount = float(amount_str)
        return True, amount
    except ValueError:
        return False, 0.0

def validate_date(date_str):
    """
    Validate a date string in the format DD.MM.YYYY.
    
    Args:
        date_str (str): Date string to validate
        
    Returns:
        (bool, datetime): (is_valid, parsed_date)
    """
    if not date_str:
        return False, None
    
    try:
        day, month, year = date_str.split('.')
        date = datetime(int(year), int(month), int(day))
        return True, date
    except (ValueError, AttributeError, TypeError):
        try:

            formats = [
                '%d.%m.%Y',
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y' 
            ]
            
            for fmt in formats:
                try:
                    date = datetime.strptime(date_str, fmt)
                    return True, date
                except ValueError:
                    continue
            
            return False, None
        except Exception:
            return False, None