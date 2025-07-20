from functools import wraps
from flask import request, jsonify
from app.utils.security import decode_access_token
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "error": "No Bearer token"}), 401
            
        token = auth_header.replace("Bearer ", "")

        try:
            payload = decode_access_token(token)
            request.user_id = payload["user_id"]
        except ExpiredSignatureError:
            print("[AUTH] Token expired")
            return jsonify({"success": False, "error": "Token expired"}), 401
        except InvalidTokenError as e:
            print(f"[AUTH] JWT error: {e}")
            return jsonify({"success": False, "error": "Invalid token"}), 401
        except Exception as e:
            print(f"[AUTH] Unexpected error: {e}")
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        return f(*args, **kwargs)
    return wrapper