class Category:
    def __init__(self, name, mcc_code=None):
        """
        Initialize a Category instance.
        
        Args:
            name (str): Category name
            mcc_code (int, optional): Merchant Category Code for mapping with bank data
        """
        self.name = name
        self.mcc_code = mcc_code
    
    def to_dict(self):
        """
        Convert the category to a dictionary for storage.
        
        Returns:
            dict: Dictionary representation of the category
        """
        return {
            "name": self.name,
            "mcc_code": self.mcc_code,
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
            name=data.get("name", ""),
            mcc_code=data.get("mcc_code")
        )
    
    def __str__(self):
        """
        Get a string representation of the category.
        
        Returns:
            str: String representation
        """
        return f"{self.name}"