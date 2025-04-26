class User:
    def __init__(self, user_id, name, email, balance=0.0, token=None):
        """
        Initialize a User instance.
        
        Args:
            user_id (str): Unique identifier for the user
            name (str): User's name
            email (str): User's email address
            balance (float): User's account balance
            token (str, optional): MonoBank API token
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.balance = balance
        self.token = token
    
    def to_dict(self):
        """
        Convert the user to a dictionary for storage.
        
        Returns:
            dict: Dictionary representation of the user
        """
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'balance': self.balance,
            'token': self.token
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a User instance from a dictionary.
        
        Args:
            data (dict): Dictionary with user data
            
        Returns:
            User: New User instance
        """
        if not data:
            return None
        
        return cls(
            user_id=data.get('user_id'),
            name=data.get('name'),
            email=data.get('email'),
            balance=data.get('balance', 0.0),
            token=data.get('token')
        )
    
    def has_monobank_token(self):
        """
        Check if the user has a MonoBank API token.
        
        Returns:
            bool: True if the user has a token, False otherwise
        """
        return bool(self.token)