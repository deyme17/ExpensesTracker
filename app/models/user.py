from app.utils.encryption import Encryption as enc

class User:
    def __init__(self, user_id: str, name: str, email: str, token: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._encrypted_token = enc.encrypt(token)

    @property
    def token(self) -> str:
        return enc.decrypt(self._encrypted_token)

    def to_dict(self) -> dict:
        if not all([self.user_id, self.name, self.email, self._encrypted_token]):
            raise ValueError("User object has missing or None fields")
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "encrypted_token": self._encrypted_token,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        token_encrypted = data.get("encrypted_token")
        if not token_encrypted:
            raise ValueError("Encrypted token missing in user data.")
        token = enc.decrypt(token_encrypted)

        return cls(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            token=token
        )

    @classmethod
    def from_api_dict(cls, data: dict) -> 'User':
        required_fields = ["user_id", "name", "email", "token"]
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f"Missing or None field: {field} in API response: {data}")
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            token=data["token"]
        )
