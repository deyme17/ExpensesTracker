import requests
from datetime import datetime, timedelta
import json

class MonobankService:
    BASE_URL = "https://api.monobank.ua"
    
    def __init__(self):
        """Init the Monobank service."""
        self.cached_client_info = None
        self.cached_transactions = {}
        self.last_request_time = None
    
    def get_client_info(self, token):
        """
        Get client information from Monobank API.
        
        Args:
            token (str): Monobank API token
            
        Returns:
            dict: Client information, or None on failure
        """
        if not token:
            return None
        
        # lims
        current_time = datetime.now()
        if self.last_request_time and (current_time - self.last_request_time).total_seconds() < 60:

            if self.cached_client_info:
                return self.cached_client_info

            return None
        
        self.last_request_time = current_time
        
        try:
            headers = {"X-Token": token}
            response = requests.get(f"{self.BASE_URL}/personal/client-info", headers=headers)
            
            if response.status_code == 200:
                self.cached_client_info = response.json()
                return self.cached_client_info
            else:
                print(f"Error getting client info: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Exception getting client info: {str(e)}")
            return None
    
    def get_transactions(self, token, account_id=None, from_time=None, to_time=None):
        """
        Get transactions from Monobank API.
        
        Args:
            token (str): Monobank API token
            account_id (str, optional): Account ID to get transactions for
            from_time (datetime, optional): Start time for transactions
            to_time (datetime, optional): End time for transactions
            
        Returns:
            list: List of transaction dictionaries, or None on failure
        """
        if not token:
            return None
        
        # lims
        current_time = datetime.now()
        if self.last_request_time and (current_time - self.last_request_time).total_seconds() < 60:

            if account_id in self.cached_transactions:
                return self.cached_transactions[account_id]

            return None
        
        self.last_request_time = current_time
        
        if not account_id:
            client_info = self.get_client_info(token)
            if not client_info or 'accounts' not in client_info or not client_info['accounts']:
                return None
            account_id = client_info['accounts'][0]['id']
        
        if not from_time:
            # default to 100 days ago
            from_time = int((current_time - timedelta(days=100)).timestamp())
        elif isinstance(from_time, datetime):
            from_time = int(from_time.timestamp())
        
        if to_time and isinstance(to_time, datetime):
            to_time = int(to_time.timestamp())
        
        url = f"{self.BASE_URL}/personal/statement/{account_id}/{from_time}"
        if to_time:
            url += f"/{to_time}"
        
        try:
            headers = {"X-Token": token}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                transactions = response.json()
                self.cached_transactions[account_id] = transactions
                return transactions
            else:
                print(f"Error getting transactions: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Exception getting transactions: {str(e)}")
            return None
    
    def get_account_balance(self, token, account_id=None):
        """
        Get account balance from Monobank API.
        
        Args:
            token (str): Monobank API token
            account_id (str, optional): Account ID to get balance for
            
        Returns:
            float: Account balance, or None on failure
        """
        client_info = self.get_client_info(token)
        if not client_info or 'accounts' not in client_info or not client_info['accounts']:
            return None
        
        # find the account
        accounts = client_info['accounts']
        if account_id:
            for account in accounts:
                if account.get('id') == account_id:
                    return account.get('balance', 0) / 100.0
        
        return accounts[0].get('balance', 0) / 100.0 
    
    def _format_transaction(self, transaction):
        """
        Format a transaction from Monobank API to a more usable format.
        
        Args:
            transaction (dict): Transaction data from Monobank API
            
        Returns:
            dict: Formatted transaction data
        """
        amount = transaction.get('amount', 0) / 100.0
        is_income = amount > 0
        
        # format date
        if 'time' in transaction:
            date = datetime.fromtimestamp(transaction['time'])
        else:
            date = datetime.now()
        
        return {
            'id': transaction.get('id', ''),
            'amount': amount,
            'date': date,
            'description': transaction.get('description', ''),
            'is_income': is_income,
            'mcc': transaction.get('mcc', 0),
            'original_mcc': transaction.get('originalMcc', 0),
            'currency_code': transaction.get('currencyCode', 980),  # UAH
            'commission_rate': transaction.get('commissionRate', 0) / 100.0,
            'cashback_amount': transaction.get('cashbackAmount', 0) / 100.0
        }