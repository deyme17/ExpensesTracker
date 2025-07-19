import re
from datetime import datetime


class ValidationError(Exception):
    pass

def validate_email(email: str):
    if not email:
        raise ValidationError("email_required")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("email_invalid")

def validate_password(password: str):
    if not password:
        raise ValidationError("password_required")
    if len(password) < 6:
        raise ValidationError("password_too_short")
    if not any(char.isdigit() for char in password):
        raise ValidationError("password_needs_digit")
    if not any(char.isalpha() for char in password):
        raise ValidationError("password_needs_letter")

def validate_monobank_token(token: str):
    if not token:
        raise ValidationError("token_missing")
    pattern = r'^[a-zA-Z0-9]{44}$'
    if not re.fullmatch(pattern, token):
        raise ValidationError("invalid_token_format")

def validate_amount(amount):
    try:
        value = float(amount)
    except (ValueError, TypeError):
        raise ValidationError("amount_invalid")
    if value <= 0:
        raise ValidationError("amount_must_be_positive")
    return value

def validate_date(date_str: str):
    if not date_str:
        raise ValidationError("date_required")
    formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValidationError("invalid_date_format")

def validate_registration_inputs(data: dict):
    email = data.get("email", "").strip()
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    token = data.get("encrypted_token", "").strip()

    validate_email(email)
    validate_password(password)
    if password != confirm_password:
        raise ValidationError("password_mismatch")
    validate_monobank_token(token)