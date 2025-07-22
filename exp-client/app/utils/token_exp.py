import jwt
from datetime import datetime

def is_token_expired(token: str) -> bool:
    """
    Checks if a JWT token is expired.
    Args:
        token: JWT token string
    Returns:
        bool: True if token is expired or invalid, False otherwise
    """
    if not token:
        return True
    
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = payload.get('exp')
        
        if not exp_timestamp:
            return True
    
        current_time = datetime.now().timestamp()
        return current_time > exp_timestamp
        
    except Exception:
        return True

def get_token_user_id(token: str) -> str|None:
    """
    Extracts user_id from JWT token without verification.
    Args:
        token: JWT token string
    Returns:
        str: user_id if found, None otherwise
    """
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get('user_id')
    except Exception:
        return None

def get_token_info(token: str) -> dict:
    """
    Gets token information for debugging.
    Args:
        token: JWT token string
    Returns:
        dict: Token information
    """
    if not token:
        return {"valid": False, "error": "No token"}
    
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = payload.get('exp', 0)
        exp_time = datetime.fromtimestamp(exp_timestamp) if exp_timestamp else None
        current_time = datetime.now()
        
        return {
            "valid": True,
            "user_id": payload.get('user_id'),
            "expires_at": exp_time.isoformat() if exp_time else None,
            "current_time": current_time.isoformat(),
            "is_expired": current_time.timestamp() > exp_timestamp if exp_timestamp else True,
            "payload": payload
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}