from flask import Blueprint, request, jsonify
from app.utils.auth_decorator import require_auth
from app.services.crud import transaction_service, account_service, category_service, currency_service, user_service

import logging
logger = logging.getLogger(__name__)

api = Blueprint("api", __name__, url_prefix="/api")


# user
@api.route("/me", methods=["GET"])
@require_auth
def get_current_user():
    logger.info(f"[GET /me] Request started for user_id: {request.user_id}")
    try:
        user = user_service.get_user_by_id(request.user_id)
        logger.info(f"[GET /me] Successfully retrieved user data for user_id: {request.user_id}")
        return jsonify({"success": True, "data": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }})
    except Exception as e:
        logger.error(f"[GET /me] Error retrieving user {request.user_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 401


# transactions
@api.route("/transactions/<user_id>", methods=["GET"])
@require_auth
def get_transactions(user_id):
    logger.info(f"[GET /transactions] Request started for user_id: {user_id}, authenticated as: {request.user_id}")
    
    try:
        if request.user_id != user_id:
            logger.warning(f"[GET /transactions] Access denied - user {request.user_id} tried to access transactions of user {user_id}")
            return jsonify({"success": False, "error": "Access denied"}), 403
        
        transactions = transaction_service.get_all_by_user(user_id)
        logger.info(f"[GET /transactions] Successfully retrieved {len(transactions)} transactions for user {user_id}")
        
        if transactions:
            logger.debug(f"[GET /transactions] Last transaction: {transactions[-1]}")
        
        return jsonify({"success": True, "data": transactions})
    
    except Exception as e:
        logger.error(f"[GET /transactions] Error retrieving transactions for user {user_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/transaction", methods=["POST"])
@require_auth
def create_transaction():
    logger.info(f"[POST /transaction] Request started for user_id: {request.user_id}")
    
    try:
        data = request.get_json()
        if not data:
            logger.warning(f"[POST /transaction] No data provided by user {request.user_id}")
            return jsonify({"success": False, "error": "No data provided"}), 400

        logger.debug(f"[POST /transaction] Request data: {data}")
        data["user_id"] = request.user_id
        
        transaction = transaction_service.create(data)
        logger.info(f"[POST /transaction] Successfully created transaction {transaction.transaction_id} for user {request.user_id}")
        
        return jsonify({"success": True, "data": {"transaction_id": transaction.transaction_id}})
    
    except KeyError as e:
        logger.error(f"[POST /transaction] Missing required field for user {request.user_id}: {str(e)}")
        return jsonify({"success": False, "error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        logger.error(f"[POST /transaction] Value error for user {request.user_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error(f"[POST /transaction] Unexpected error for user {request.user_id}: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@api.route("/transaction/<string:transaction_id>", methods=["PATCH"])
@require_auth
def update_transaction(transaction_id):
    logger.info(f"[PATCH /transaction] Request started for transaction_id: {transaction_id}, user_id: {request.user_id}")
    
    try:
        data = request.get_json()
        if not data:
            logger.warning(f"[PATCH /transaction] No data provided for transaction {transaction_id} by user {request.user_id}")
            return jsonify({"success": False, "error": "No data provided"}), 400

        logger.debug(f"[PATCH /transaction] Update data for transaction {transaction_id}: {data}")
        
        transaction_service.update(transaction_id, data)
        logger.info(f"[PATCH /transaction] Successfully updated transaction {transaction_id} by user {request.user_id}")
        
        return jsonify({"success": True})
    
    except KeyError as e:
        logger.error(f"[PATCH /transaction] Transaction {transaction_id} not found for user {request.user_id}")
        return jsonify({"success": False, "error": f"Transaction not found: {transaction_id}"}), 404
    except ValueError as e:
        logger.error(f"[PATCH /transaction] Value error updating transaction {transaction_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        logger.error(f"[PATCH /transaction] Unexpected error updating transaction {transaction_id}: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@api.route("/transaction/<string:transaction_id>", methods=["DELETE"])
@require_auth
def delete_transaction(transaction_id):
    logger.info(f"[DELETE /transaction] Request started for transaction_id: {transaction_id}, user_id: {request.user_id}")
    
    try:
        transaction_service.delete(transaction_id)
        logger.info(f"[DELETE /transaction] Successfully deleted transaction {transaction_id} by user {request.user_id}")
        
        return jsonify({"success": True})
    
    except KeyError as e:
        logger.error(f"[DELETE /transaction] Transaction {transaction_id} not found for user {request.user_id}")
        return jsonify({"success": False, "error": f"Transaction not found: {transaction_id}"}), 404
    except Exception as e:
        logger.error(f"[DELETE /transaction] Unexpected error deleting transaction {transaction_id}: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500
    

# accounts
@api.route("/accounts", methods=["POST"])
def create_account():
    logger.info("[POST /accounts] Account creation request started")
    
    try:
        data = request.get_json()
        logger.debug(f"[POST /accounts] Request data: {data}")
        
        account = account_service.create(data)
        logger.info(f"[POST /accounts] Successfully created account {account.account_id}")
        
        return jsonify({"success": True, "data": {"account_id": account.account_id}})

    except Exception as e:
        logger.error(f"[POST /accounts] Error creating account: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400


@api.route("/accounts/<user_id>", methods=["GET"])
@require_auth
def get_accounts(user_id):
    logger.info(f"[GET /accounts] Request started for user_id: {user_id}, authenticated as: {request.user_id}")
    
    if request.user_id != user_id:
        logger.warning(f"[GET /accounts] Access denied - user {request.user_id} tried to access accounts of user {user_id}")
        return jsonify({"success": False, "error": "Access denied"}), 403
    
    try:
        accounts = account_service.get_by_user_id(user_id)
        logger.info(f"[GET /accounts] Successfully retrieved {len(accounts)} accounts for user {user_id}")
        
        if accounts:
            logger.debug(f"[GET /accounts] Last account: {accounts[-1]}")
        
        return jsonify({"success": True, "data": accounts})
    
    except Exception as e:
        logger.error(f"[GET /accounts] Error retrieving accounts for user {user_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
    

# categories
@api.route("/categories", methods=["GET"])
def get_categories():
    logger.info("[GET /categories] Request started")
    
    try:
        categories = category_service.get_all()
        logger.info(f"[GET /categories] Successfully retrieved {len(categories)} categories")
        
        if categories:
            logger.debug(f"[GET /categories] Last category: {categories[-1]}")
        
        return jsonify({"success": True, "data": categories})
    except Exception as e:
        logger.error(f"[GET /categories] Error retrieving categories: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400


# currencies
@api.route("/currencies", methods=["GET"])
def get_currencies():
    logger.info("[GET /currencies] Request started")
    
    try:
        currencies = currency_service.get_all()
        logger.info(f"[GET /currencies] Successfully retrieved {len(currencies)} currencies")
        
        if currencies:
            logger.debug(f"[GET /currencies] Last currency: {currencies[-1]}")
        
        return jsonify({"success": True, "data": currencies})
    except Exception as e:
        logger.error(f"[GET /currencies] Error retrieving currencies: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400