import requests
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class BankService(ABC):
    def __init__(self, token):
        if not token:
            raise ValueError("API token is required.")
        self.token = token

    def _headers(self):
        return {"X-Token": self.token}

    @abstractmethod
    def get_client_info(self):
        """
        Get the necessary information to create a user in the database.
        
        Returns:
            dict: {
            "user_id": str,
            "name": str,
            "balance": float
        }
        """
        pass

    @abstractmethod
    def get_transactions(self, account_id=None, days=100):
        """
        Import user transactions for the last N days.

        Returns:
            dict: {
                "transaction_id": str,
                "user_id": str,
                "amount": float,
                "date": datetime.date,
                "currency_code": int,
                "mcc_code": int,
                "type": str,
                "description": str,
                "cashback": float,
                "commission": float
            }
        """
        pass