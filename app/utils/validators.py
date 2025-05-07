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
    
    if len(password) < 6:
        return False, "Пароль має містити щонайменше 6 символів"
    
    has_digit = any(char.isdigit() for char in password)
    if not has_digit:
        return False, "Пароль повинен містити щонайменше одну цифру"
    
    has_letter = any(char.isalpha() for char in password)
    if not has_letter:
        return False, "Пароль повинен містити щонайменше одну дітеру"
    
    return True, ""

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

    pattern = r'^[a-zA-Z0-9]{44}$'
    return bool(re.fullmatch(pattern, token))

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
        
def validate_registration_inputs(inputs):
    """
    Validate registration inputs.

    Args:
        inputs (dict): {
            "email": str,
            "password": str,
            "confirm_password": str,
            "monobank_token": str
        }

    Returns:
        (bool, str): (is_valid, error_message)
    """
    email = inputs.get("email", "").strip()
    password = inputs.get("password", "")
    confirm_password = inputs.get("confirm_password", "")
    token = inputs.get("monobank_token", "").strip()

    if not validate_email(email):
        return False, "Некоректний email"

    if not validate_password(password):
        return False, "Пароль має містити не менше 6 символів"

    if password != confirm_password:
        return False, "Паролі не співпадають"

    if token and not validate_monobank_token(token):
        return False, "Невірний формат токену Монобанк"

    return True, ""
