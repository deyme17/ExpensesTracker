from flask import Blueprint, request, jsonify
from server.services.transaction_service import transaction_service
from server.services.account_service import account_service
from server.services.category_service import category_service
from server.services.currency_service import currency_service
from server.services.auth_service import AuthService
from server.utils.security import decode_access_token
from server.utils.auth_decorator import require_auth

api = Blueprint("api", __name__, url_prefix="/api")
auth_service = AuthService()

# user
@api.route("/me", methods=["GET"])
@require_auth
def get_current_user():
    try:
        user = auth_service.get_user_by_id(request.user_id)
        return jsonify({"success": True, "data": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401


# transactions
@api.route("/transactions/<user_id>", methods=["GET"])
@require_auth
def get_transactions(user_id):
    if request.user_id != user_id:
        return jsonify({"success": False, "error": "Access denied"}), 403

    transactions = transaction_service.get_all_by_user(user_id)
    return jsonify({"success": True, "data": transactions})


@api.route("/transaction", methods=["POST"])
@require_auth
def create_transaction():
    data = request.json
    data["user_id"] = request.user_id
    transaction = transaction_service.create(data)
    return jsonify({"success": True, "data": {"transaction_id": transaction.transaction_id}})


@api.route("/transaction/<string:transaction_id>", methods=["PATCH"])
@require_auth
def update_transaction(transaction_id):
    data = request.json
    transaction_service.update(transaction_id, data)
    return jsonify({"success": True})


@api.route("/transaction/<string:transaction_id>", methods=["DELETE"])
@require_auth
def delete_transaction(transaction_id):
    transaction_service.delete(transaction_id)
    return jsonify({"success": True})


# accounts
@api.route("/accounts", methods=["POST"])
def create_account():
    try:
        data = request.json
        account = account_service.create(data)
        return jsonify({"success": True, "data": {"account_id": account.account_id}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api.route("/accounts/<user_id>", methods=["GET"])
@require_auth
def get_accounts(user_id):
    if request.user_id != user_id:
        return jsonify({"success": False, "error": "Access denied"}), 403
    try:
        accounts = account_service.get_by_user_id(user_id)
        return jsonify({"success": True, "data": accounts})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# categories
@api.route("/categories", methods=["GET"])
def get_categories():
    try:
        return jsonify({"success": True, "data": category_service.get_all()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# currencies
@api.route("/currencies", methods=["GET"])
def get_currencies():
    try:
        return jsonify({"success": True, "data": currency_service.get_all()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400