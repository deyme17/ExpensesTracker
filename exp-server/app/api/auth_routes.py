from flask import Blueprint, request, jsonify
from app.utils.security import create_access_token
from app.services import auth_service
from app.database.db import SessionLocal

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    db = SessionLocal()
    try:
        data = request.get_json()
        user_info = auth_service.register_user(data, db)
        print(f"[DEBUG ROUTES] <register>\nUser email:\n{user_info['email']}")
        token = create_access_token({"user_id": user_info["user_id"]})

        return jsonify({
            "success": True,
            "user_id": user_info["user_id"],
            "name": user_info["name"],
            "email": user_info["email"],
            "token": token
        })
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        db.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        result = auth_service.login_user(email, password)
        print(f"[DEBUG ROUTES] <login>\nUser email:\n{result["email"]}")
        return jsonify({
            "success": True,
            "user_id": result["user_id"],
            "name": result["name"],
            "email": result["email"],
            "token": result["token"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401
    

# ping
ping_bp = Blueprint("ping", __name__)

@ping_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200
