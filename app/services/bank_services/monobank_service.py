import requests
from datetime import datetime, timedelta


class MonobankService:
    BASE_URL = "https://api.monobank.ua"

    def __init__(self, token):
        self.token = token

    def _headers(self):
        return {"X-Token": self.token}

    def get_client_info(self):
        """
        Basic information about the user is obtained, including accounts.

        Returns:
            dict: {
                "user_id": str,
                "name": str,
                "accounts": list[dict],
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
            "user_id": data.get("clientId"),
            "name": data.get("name"),
            "accounts": accounts
        }

    def get_transactions(self, account_id, days=31):
        """
        Gets transactions for a specific account for the last N days.

        Args:
            account_id (str): Monobank account ID
            days (int): How many days to get history

        Returns:
            list: list of transaction dictionaries
        """
        if not account_id:
            raise ValueError("Account ID is required")

        to_time = int(datetime.now().timestamp())
        from_time = int((datetime.now() - timedelta(days=days)).timestamp())

        url = f"{self.BASE_URL}/personal/statement/{account_id}/{from_time}/{to_time}"
        response = requests.get(url, headers=self._headers())

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 204:
            return []
        else:
            raise Exception(f"[Monobank] Transaction fetch error: {response.status_code} - {response.text}")
