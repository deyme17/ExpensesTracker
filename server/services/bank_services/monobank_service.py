import requests
import time
from datetime import datetime, timedelta
from utils.language_mapper import LanguageMapper as LM

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
            raise Exception(LM.message("client_info_error").format(
                status=response.status_code,
                text=response.text))

        data = response.json()
        accounts = data.get("accounts", [])
        if not accounts:
            raise Exception(LM.message("no_accounts_found"))

        return {
            "user_id": data.get("clientId"),
            "name": data.get("name"),
            "accounts": accounts
        }

    def get_transactions(self, account_id, days=31):
        if not account_id:
            raise ValueError(LM.message("missing_account_id"))

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
            raise Exception(LM.message("too_many_requests"))
        else:
            raise Exception(LM.message("transactions_fetch_error").format(
                status=response.status_code,
                text=response.text))
