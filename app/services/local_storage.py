import json
import os
from datetime import datetime
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category


class LocalStorageService:    
    def __init__(self, storage_dir=None):
        """
        Init the local storage service.
        
        Args:
            storage_dir (str, optional): Directory for storing data files
        """
        if storage_dir is None:
            # default dir - home folder
            home_dir = os.path.expanduser("~")
            self.storage_dir = os.path.join(home_dir, ".expenses_tracker")
        else:
            self.storage_dir = storage_dir
        
        # create storage dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        
        # define file paths
        self.user_file = os.path.join(self.storage_dir, "user.json")
        self.transactions_file = os.path.join(self.storage_dir, "transactions.json")
        self.categories_file = os.path.join(self.storage_dir, "categories.json")
    
    def save_user(self, user):
        """
        Save user data to storage.
        
        Args:
            user (User): User object to save
        """
        if not user:
            return
        
        with open(self.user_file, 'w', encoding='utf-8') as f:
            json.dump(user.to_dict(), f, ensure_ascii=False, indent=2)
    
    def get_user(self):
        """
        Load user data from storage.
        
        Returns:
            User: User object, or None if not found
        """
        if not os.path.exists(self.user_file):
            return None
        
        try:
            with open(self.user_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            return User.from_dict(user_data)
        except (json.JSONDecodeError, IOError):
            return None
    
    def clear_user(self):
        """Remove user data from storage."""
        if os.path.exists(self.user_file):
            os.remove(self.user_file)
    
    def save_transactions(self, transactions):
        """
        Save transaction data to storage.
        
        Args:
            transactions (list): List of Transaction objects to save
        """
        if not transactions:
            return
        
        transaction_dicts = [t.to_dict() for t in transactions]
        with open(self.transactions_file, 'w', encoding='utf-8') as f:
            json.dump(transaction_dicts, f, ensure_ascii=False, indent=2)
    
    def get_transactions(self, force_refresh=False):
        """
        Load transaction data from storage.
        
        Returns:
            list: List of Transaction objects, or empty list if not found
        """
        if not os.path.exists(self.transactions_file):
            return []
        
        try:
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                transaction_dicts = json.load(f)
            return [Transaction.from_dict(td) for td in transaction_dicts]
        except (json.JSONDecodeError, IOError):
            return []
    
    def add_transaction(self, transaction):
        """
        Add a single transaction to storage.
        
        Args:
            transaction (Transaction): Transaction object to add
        """
        if not transaction:
            return
        
        transactions = self.get_transactions()
        transactions.append(transaction)
        self.save_transactions(transactions)
    
    def update_transaction(self, transaction):
        """
        Update a transaction in storage.
        
        Args:
            transaction (Transaction): Updated Transaction object
        """
        if not transaction:
            return
        
        transactions = self.get_transactions()
        for i, t in enumerate(transactions):
            if t.transaction_id == transaction.transaction_id:
                transactions[i] = transaction
                break
        
        self.save_transactions(transactions)
    
    def delete_transaction(self, transaction_id):
        """
        Delete a transaction from storage.
        
        Args:
            transaction_id (str): ID of the transaction to delete
        """
        if not transaction_id:
            return
        
        transactions = self.get_transactions()
        transactions = [t for t in transactions if t.transaction_id != transaction_id]
        self.save_transactions(transactions)
    
    def get_transaction(self, transaction_id):
        """
        Get a specific transaction by ID.
        
        Args:
            transaction_id (str): ID of the transaction to get
            
        Returns:
            Transaction: Transaction object, or None if not found
        """
        if not transaction_id:
            return None
        
        transactions = self.get_transactions()
        for t in transactions:
            if t.transaction_id == transaction_id:
                return t
        
        return None
    
    def save_categories(self, categories):
        """
        Save category data to storage.
        
        Args:
            categories (list): List of Category objects to save
        """
        if not categories:
            return
        
        category_dicts = [c.to_dict() for c in categories]
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            json.dump(category_dicts, f, ensure_ascii=False, indent=2)
    
    def get_categories(self):
        """
        Load category data from storage.
        
        Returns:
            list: List of Category objects, or empty list if not found
        """
        if not os.path.exists(self.categories_file):
            return []
        
        try:
            with open(self.categories_file, 'r', encoding='utf-8') as f:
                category_dicts = json.load(f)
            return [Category.from_dict(cd) for cd in category_dicts]
        except (json.JSONDecodeError, IOError):
            return []
    
    def close(self):
        """Close the storage service and release any resources."""
        # TODO
        pass