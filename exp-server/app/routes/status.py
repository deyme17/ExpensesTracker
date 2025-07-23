from flask import Blueprint

ping_bp = Blueprint("ping", __name__)

@ping_bp.route("/", methods=["GET"])
def index():
    return "Server is up"