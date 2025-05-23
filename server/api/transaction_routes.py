from flask import Blueprint, request, jsonify
from server.services.transaction_service import TransactionService

transactions_bp = Blueprint("transactions", __name__, url_prefix="/api/transactions")
service = TransactionService()

@transactions_bp.route("", methods=["POST"])
def add_transaction():
    data = request.json
    try:
        result = service.create_transaction(data)
        return jsonify({"success": True, "id": result.transaction_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
