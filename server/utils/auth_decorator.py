from functools import wraps
from flask import request, jsonify
from server.utils.security import decode_access_token

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        try:
            payload = decode_access_token(token)
            request.user_id = payload["user_id"]
        except Exception:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        return f(*args, **kwargs)
    return wrapper