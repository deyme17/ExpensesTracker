from flask import Blueprint, request, jsonify
from app.utils.security import create_access_token
from app.services import auth_service
from app.database.db import SessionLocal

import logging
logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    logger.info("[POST /auth/register] Registration request started")
    
    db = SessionLocal()
    try:
        data = request.get_json()
        logger.debug(f"[POST /auth/register] Registration data received (email: {data.get('email', 'N/A')})")
        
        user_info = auth_service.register_user(data, db)
        logger.info(f"[POST /auth/register] User successfully registered with email: {user_info['email']}")
        
        token = create_access_token({"user_id": user_info["user_id"]})
        logger.debug(f"[POST /auth/register] Access token created for user {user_info['user_id']}")

        return jsonify({
            "success": True,
            "data": {
                "user_id": user_info["user_id"],
                "name": user_info["name"],
                "email": user_info["email"],
                "token": token
            }
        })
    except Exception as e:
        logger.error(f"[POST /auth/register] Registration failed: {str(e)}")
        db.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        db.close()
        logger.debug("[POST /auth/register] Database session closed")


@auth_bp.route("/login", methods=["POST"])
def login():
    logger.info("[POST /auth/login] Login request started")
    
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        logger.debug(f"[POST /auth/login] Login attempt for email: {email}")

        result = auth_service.login_user(email, password)
        logger.info(f"[POST /auth/login] User successfully logged in with email: {result['email']}")
        
        return jsonify({
            "success": True,
            "data": {
                "user_id": result["user_id"],
                "name": result["name"],
                "email": result["email"],
                "token": result["token"]
            }
        })
    except Exception as e:
        logger.error(f"[POST /auth/login] Login failed for email {email if 'email' in locals() else 'unknown'}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 401