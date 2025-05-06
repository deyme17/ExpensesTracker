import requests
from datetime import datetime, timedelta
from app.services.bank_services.bank_service import BankService


class MonobankService(BankService):
    BASE_URL = "https://api.monobank.ua"

    def _headers(self):
        return {"X-Token": self.token}

    def get_client_info(self):
        """
        Get the necessary information to create a user in the database.
        
        Returns:
            dict: {
                "user_id": Monobank ID,
                "name": user name,
                "balance": current balance
            }
        """
        url = f"{self.BASE_URL}/personal/client-info"
        response = requests.get(url, headers=self._headers())

        if response.status_code != 200:
            raise Exception(f"[Monobank] Client info error: {response.status_code} - {response.text}")
        
        data = response.json()
        accounts = data.get("accounts", [])
        if not accounts:
            raise Exception("[Monobank] No accounts found for client.")

        return {
            "user_id": data["clientId"],
            "name": data["name"],
            "balance": accounts[0]["balance"] / 100.0
        }


    def get_transactions(self, account_id=None, days=100):
        """
        Import user transactions for the last N days.

        Returns:
            List of formatted transaction dictionaries.
        """
        client_info = self.get_client_info()
        if not account_id:
            accounts = client_info.get("accounts", [])
            if not accounts:
                raise Exception("[Monobank] No accounts found for client.")
            account_id = accounts[0]["id"]

        from_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())
        url = f"{self.BASE_URL}/personal/statement/{account_id}/{from_timestamp}"
        response = requests.get(url, headers=self._headers())

        if response.status_code == 200:
            raw_transactions = response.json()
            return [self._format_transaction(tx, client_info["clientId"]) for tx in raw_transactions]
        raise Exception(f"[Monobank] Transactions error: {response.status_code} - {response.text}")

    def _format_transaction(self, tx, user_id):
        """
        Formats the transaction for saving to the database.
        """
        amount = tx.get("amount", 0) / 100.0
        timestamp = tx.get("time", int(datetime.now().timestamp()))
        date = datetime.fromtimestamp(timestamp)

        return {
            "transaction_id": tx.get("id"),
            "user_id": user_id,
            "amount": amount,
            "date": date.date(),
            "currency_code": tx.get("currencyCode", 980),
            "mcc_code": tx.get("mcc", 0),
            "type": "card",
            "description": tx.get("description", "Without_description"),
            "cashback": tx.get("cashbackAmount", 0) / 100.0,
            "commission": tx.get("commissionRate", 0) / 100.0
        }

