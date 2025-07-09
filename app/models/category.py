class Category:
    def __init__(self, name: str, mcc_code: int|str):
        self.name = name
        self.mcc_code = int(mcc_code)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "mcc_code": self.mcc_code,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        if not data:
            return None
        
        return cls(
            name=data.get("name", ""),
            mcc_code=data.get("mcc_code")
        )
    
    def __str__(self) -> str:
        return f"{self.name}"