from flask import Blueprint, request, jsonify
from server.services import auth_service
from server.utils.security import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        user_info = auth_service.register_user(data)

        token = create_access_token({"user_id": user_info["user_id"]})

        return jsonify({
            "success": True,
            "user_id": user_info["user_id"],
            "name": user_info["name"],
            "email": user_info["email"],
            "token": token
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        result = auth_service.login_user(email, password)

        return jsonify({
            "success": True,
            "user_id": result["user_id"],
            "name": result["name"],
            "email": result["email"],
            "token": result["token"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401
    
ping_bp = Blueprint("ping", __name__)

@ping_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200
