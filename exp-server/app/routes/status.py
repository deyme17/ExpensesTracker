from flask import Blueprint

status_bp = Blueprint("ping", __name__)

@status_bp.route("/", methods=["GET"])
def index():
    return "Server is up"