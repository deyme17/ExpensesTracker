from flask import Blueprint, request, jsonify
from server.services.transaction_service import transaction_service
from server.services.account_service import account_service
from server.services.category_service import category_service
from server.services.currency_service import currency_service
from server.services.auth_service import AuthService
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
    try:
        if request.user_id != user_id:
            return jsonify({"success": False, "error": "Access denied"}), 403
        
        transactions = transaction_service.get_all_by_user(user_id)
        return jsonify({"success": True, "data": transactions})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/transaction", methods=["POST"])
@require_auth
def create_transaction():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        data["user_id"] = request.user_id
        transaction = transaction_service.create(data)
        return jsonify({"success": True, "data": {"transaction_id": transaction.transaction_id}})
    
    except KeyError as e:
        return jsonify({"success": False, "error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500


@api.route("/transaction/<string:transaction_id>", methods=["PATCH"])
@require_auth
def update_transaction(transaction_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        transaction_service.update(transaction_id, data)
        return jsonify({"success": True})
    
    except KeyError as e:
        return jsonify({"success": False, "error": f"Transaction not found: {transaction_id}"}), 404
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500


@api.route("/transaction/<string:transaction_id>", methods=["DELETE"])
@require_auth
def delete_transaction(transaction_id):
    try:
        transaction_service.delete(transaction_id)
        return jsonify({"success": True})
    
    except KeyError as e:
        return jsonify({"success": False, "error": f"Transaction not found: {transaction_id}"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500
    

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
    
@api.route("/accounts/<account_id>", methods=["PATCH"])
@require_auth
def update_balance(account_id):
    data = request.json
    if not data or "val" not in data:
        return jsonify({"error": "Missing 'val' in request body"}), 400
    try:
        account_service.update_balance(account_id, data["val"])
        return jsonify({"success": True})
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


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