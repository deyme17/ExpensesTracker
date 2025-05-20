from flask import Blueprint, request, jsonify
from server.services import user_service, transaction_service, account_service, category_service, currency_service
from server.utils.security import create_access_token

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        user = user_service.register(data)
        token = create_access_token({"user_id": user.user_id})

        return jsonify({
            "success": True,
            "token": token,
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "balance": float(user.balance)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    

@api.route("/transactions/<user_id>", methods=["GET"])
def get_transactions(user_id):
    return jsonify(transaction_service.get_all_by_user(user_id))

@api.route("/transaction", methods=["POST"])
def create_transaction():
    try:
        data = request.json
        transaction = transaction_service.create(data)
        return jsonify({"success": True, "id": transaction.transaction_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api.route("/transaction/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    try:
        transaction_service.delete(transaction_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api.route("/transaction/<int:transaction_id>", methods=["PATCH"])
def update_transaction(transaction_id):
    try:
        data = request.json
        transaction_service.update(transaction_id, data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api.route("/accounts", methods=["POST"])
def create_account():
    try:
        data = request.json
        account = account_service.create(data)
        return jsonify({"success": True, "account_id": account.account_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api.route("/categories", methods=["GET"])
def get_categories():
    return jsonify(category_service.get_all())

@api.route("/currencies", methods=["GET"])
def get_currencies():
    return jsonify(currency_service.get_all())
