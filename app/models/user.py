import hashlib
from app.utils.encryption_service import EncryptionService

class User:
    def __init__(self, user_id, name, email, token, password_hash):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._encrypted_token = EncryptionService.encrypt(token)
        self.password_hash = password_hash

    @property
    def token(self):
        return EncryptionService.decrypt(self._encrypted_token)

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "encrypted_token": self._encrypted_token,
            "password_hash": self.password_hash
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
            token=token,
            password_hash=data.get("password_hash")
        )
