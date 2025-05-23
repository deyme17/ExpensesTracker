from flask import Blueprint, request, jsonify
from server.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth = AuthService()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        user = auth.register_user(data)
        return jsonify({"success": True, "user_id": user.user_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    try:
        result = auth.login_user(data["email"], data["password"])
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401
