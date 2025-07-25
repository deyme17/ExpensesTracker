import re
from app.utils.language_mapper import LanguageMapper as LM
from datetime import datetime


def validate_email(email):
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    if not password:
        return False, LM.message("password_required")

    if len(password) < 6:
        return False, LM.message("password_too_short")

    has_digit = any(char.isdigit() for char in password)
    if not has_digit:
        return False, LM.message("password_needs_digit")

    has_letter = any(char.isalpha() for char in password)
    if not has_letter:
        return False, LM.message("password_needs_letter")

    return True, ""


def validate_monobank_token(token):
    if not token or not isinstance(token, str):
        return False
    return bool(re.fullmatch(r'^[a-zA-Z0-9\-_]{40,50}$', token))


def validate_amount(amount_str):
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
    if not date_str:
        return False, None

    try:
        day, month, year = date_str.split('.')
        date = datetime(int(year), int(month), int(day))
        return True, date
    except (ValueError, AttributeError, TypeError):
        formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']
        for fmt in formats:
            try:
                date = datetime.strptime(date_str, fmt)
                return True, date
            except ValueError:
                continue
        return False, None


def validate_registration_inputs(inputs):
    email = inputs.get("email", "").strip()
    password = inputs.get("password", "")
    confirm_password = inputs.get("confirm_password", "")
    token = inputs.get("monobank_token", "").strip()

    if not validate_email(email):
        return False, LM.message("email_invalid")

    valid, msg = validate_password(password)
    if not valid:
        return False, msg

    if password != confirm_password:
        return False, LM.message("password_mismatch")

    if token and not validate_monobank_token(token):
        return False, LM.message("invalid_token_format")

    return True, ""

def validate_transaction_inputs(inputs):
    from app.utils.language_mapper import LanguageMapper as LM
    import traceback

    try:
        valid_amount, amount = validate_amount(inputs.get("amount", ""))
        valid_cashback, cashback = validate_amount(inputs.get("cashback", "0"))
        valid_commission, commission = validate_amount(inputs.get("commission", "0"))

        if not valid_amount or amount == 0:
            return False, LM.server_error("nonzero_amount")
        if not valid_cashback or cashback < 0:
            return False, LM.server_error("positive_cashback")
        if not valid_commission or commission < 0:
            return False, LM.server_error("positive_commission")

        return True, ""
    except Exception:
        import traceback
        traceback.print_exc()
        return False, LM.server_error("unknown_error")
