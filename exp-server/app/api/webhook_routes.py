from flask import Blueprint, request, jsonify
from app.tasks.webhook_tasks import handle_webhook_task

mono_webhook_bp = Blueprint("monobank_webhook", __name__, url_prefix="/api/monobank")


@mono_webhook_bp.route("/webhook", methods=["POST"])
def monobank_webhook():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "rejected"}), 400

        handle_webhook_task.delay(data=data, bank_name="monobank")

        return jsonify({"status": "accepted"}), 202

    except Exception as e:
        return jsonify({"status": "rejected", "error": str(e)}), 500