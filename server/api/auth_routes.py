from flask import Blueprint, request, jsonify
from server.services import user_service
from server.utils.security import verify_password

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        user, token = user_service.register(data)
        return jsonify({
            "success": True,
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "token": token,
            "password_hash": user.hashed_password
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = user_service.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise Exception("Невірний email або пароль")

        token = user_service.create_token(user)
        return jsonify({
            "success": True,
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "token": token,
            "password_hash": user.hashed_password
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401