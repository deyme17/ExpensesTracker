from datetime import datetime


class Transaction:
    def __init__(self, transaction_id, user_id, amount, date, category, description,
                is_income, payment_method, currency='UAH', cashback=0, commission=0, 
                is_synced=True):
        """
        Initialize a Transaction instance.
        
        Args:
            transaction_id (str): Unique identifier for the transaction
            user_id (str): ID of the user who owns the transaction
            amount (float): Transaction amount (positive for income, negative for expense)
            date (datetime): Date and time of the transaction
            category (str): Transaction category
            description (str): Transaction description
            is_income (bool): Whether the transaction is income (True) or expense (False)
            payment_method (str): Payment method ('Картка' or 'Готівка')
            currency (str): Currency code (default 'UAH')
            cashback (float): Cashback amount
            commission (float): Commission amount
        """
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = float(amount)
        
        if isinstance(date, str):
            try:
                # parse common date formats
                self.date = datetime.strptime(date, '%d.%m.%Y')
            except ValueError:
                try:
                    self.date = datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    self.date = datetime.now()
        else:
            self.date = date
        
        self.category = category
        self.description = description
        self.is_income = is_income
        self.payment_method = payment_method
        self.currency = currency
        self.cashback = float(cashback)
        self.commission = float(commission)
        self.is_synced = is_synced
    
    def to_dict(self):
        """
        Convert the transaction to a dictionary for storage.
        
        Returns:
            dict: Dictionary representation of the transaction
        """
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'date': self.date.isoformat(),
            'category': self.category,
            'description': self.description,
            'is_income': self.is_income,
            'payment_method': self.payment_method,
            'currency': self.currency,
            'cashback': self.cashback,
            'commission': self.commission,
            'is_synced': self.is_synced
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Transaction instance from a dictionary.
        
        Args:
            data (dict): Dictionary with transaction data
            
        Returns:
            Transaction: New Transaction instance
        """
        if not data:
            return None
        
        # parse date from ISO format
        date = data.get('date')
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                date = datetime.now()
        
        return cls(
            transaction_id=data.get('transaction_id'),
            user_id=data.get('user_id'),
            amount=data.get('amount', 0.0),
            date=date,
            category=data.get('category', ''),
            description=data.get('description', ''),
            is_income=data.get('is_income', False),
            payment_method=data.get('payment_method', 'Картка'),
            currency=data.get('currency', 'UAH'),
            cashback=data.get('cashback', 0.0),
            commission=data.get('commission', 0.0),
            is_synced=data.get('is_synced', True)
        )
    
    def get_formatted_amount(self):
        """
        Get a formatted string representation of the transaction amount.
        
        Returns:
            str: Formatted amount string (with +/- sign and currency)
        """
        sign = '+' if self.is_income else '-'
        return f"{sign}{abs(self.amount):,.2f} {self.currency}"
    
    def get_formatted_date(self):
        """
        Get a formatted string representation of the transaction date.
        
        Returns:
            str: Formatted date string (DD.MM.YYYY)
        """
        return self.date.strftime('%d.%m.%Y')
    
    def __str__(self):
        """
        Get a string representation of the transaction.
        
        Returns:
            str: String representation
        """
        return f"{self.get_formatted_date()} | {self.category} | {self.get_formatted_amount()}"