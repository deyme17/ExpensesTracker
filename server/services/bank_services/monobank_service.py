import requests
import time
from datetime import datetime, timedelta

class MonobankService:
    BASE_URL = "https://api.monobank.ua"

    def __init__(self, token):
        self.token = token

    def _headers(self):
        return {"X-Token": self.token}

    def get_client_info(self):
        url = f"{self.BASE_URL}/personal/client-info"
        response = requests.get(url, headers=self._headers())

        if response.status_code != 200:
            raise Exception("client_info_error: status={status}, text={text}".format(
                status=response.status_code,
                text=response.text))

        data = response.json()
        accounts = data.get("accounts", [])
        if not accounts:
            raise Exception("no_accounts_found")

        return {
            "user_id": data.get("clientId"),
            "name": data.get("name"),
            "accounts": accounts
        }

    def get_transactions(self, account_id, days=31):
        if not account_id:
            raise ValueError("missing_account_id")

        to_time = int(datetime.now().timestamp())
        from_time = int((datetime.now() - timedelta(days=days)).timestamp())

        url = f"{self.BASE_URL}/personal/statement/{account_id}/{from_time}/{to_time}"

        time.sleep(0.4)

        response = requests.get(url, headers=self._headers())

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 204:
            return []
        elif response.status_code == 429:
            raise Exception("too_many_requests")
        else:
            raise Exception("transactions_fetch_error: status={status}, text={text}".format(
                status=response.status_code,
                text=response.text))
        
    def set_webHook(self, url: str) -> None:
        """
        Sets WebHookURL for current user.
        Args:
            url: WebHook endpoint on which the updates will be sent.
        """
        response = requests.post(
            f"{self.BASE_URL}/personal/webhook",
            headers=self._headers(),
            json={"webHookUrl": url}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to set webHook {response.text}")