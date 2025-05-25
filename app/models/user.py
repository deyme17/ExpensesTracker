import hashlib
from app.utils.encryption import EncryptionService

class User:
    def __init__(self, user_id, name, email, token):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._encrypted_token = EncryptionService.encrypt(token)

    @property
    def token(self):
        return EncryptionService.decrypt(self._encrypted_token)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "encrypted_token": self._encrypted_token,
        }

    @classmethod
    def from_dict(cls, data):
        token_encrypted = data.get("encrypted_token")
        if not token_encrypted:
            raise ValueError("Encrypted token missing in user data.")
        token = EncryptionService.decrypt(token_encrypted)

        return cls(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            token=token
        )

    @classmethod
    def from_api_dict(cls, data):
        token = data.get("token") or data.get("encrypted_token") or ""
        return cls(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            token=token
        )
