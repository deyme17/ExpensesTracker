from flask import Blueprint, request, jsonify
from server.services.webhook_services import mono_webhook_service
from server.database.db import SessionLocal

mono_webhook_bp = Blueprint("monobank_webhook", __name__, url_prefix="/api/monobank")



@mono_webhook_bp.route("/webhook", methods=["POST"])
def monobank_webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no_data"}), 400

    session = SessionLocal()
    try:
        mono_webhook_service.save_hooked_transactions(data, session)
        session.commit()
        return jsonify({"success": True}), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        session.close()