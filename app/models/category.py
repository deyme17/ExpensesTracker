class Category:
    def __init__(self, name, is_income, mcc_code=None, color=None):
        """
        Initialize a Category instance.
        
        Args:
            name (str): Category name
            is_income (bool): Whether this is an income category
            mcc_code (int, optional): Merchant Category Code for mapping with bank data
            color (str, optional): Color hex code for the category
        """
        self.name = name
        self.is_income = is_income
        self.mcc_code = mcc_code
        self.color = color 
    
    def to_dict(self):
        """
        Convert the category to a dictionary for storage.
        
        Returns:
            dict: Dictionary representation of the category
        """
        return {
            'name': self.name,
            'is_income': self.is_income,
            'mcc_code': self.mcc_code,
            'color': self.color
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Category instance from a dictionary.
        
        Args:
            data (dict): Dictionary with category data
            
        Returns:
            Category: New Category instance
        """
        if not data:
            return None
        
        return cls(
            name=data.get('name', ''),
            is_income=data.get('is_income', False),
            mcc_code=data.get('mcc_code'),
            color=data.get('color')
        )
    
    def __str__(self):
        """
        Get a string representation of the category.
        
        Returns:
            str: String representation
        """
        return f"{self.name} ({'Дохід' if self.is_income else 'Витрата'})"