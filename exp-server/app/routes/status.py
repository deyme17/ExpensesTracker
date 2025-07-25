from flask import Blueprint, jsonify

ping_bp = Blueprint("ping", __name__)

@ping_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200


status_bp = Blueprint("status", __name__)

@status_bp.route("/", methods=["GET"])
def index():
    return "Server is up"