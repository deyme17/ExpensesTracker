import os
from pathlib import Path
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

class Encryption:
    ENV_PATH = Path(".env")
    ENV_KEY_NAME = "FERNET_KEY"
    _fernet = None

    @classmethod
    def _initialize(cls):
        if not cls.ENV_PATH.exists():
            cls.ENV_PATH.write_text("")

        load_dotenv(dotenv_path=cls.ENV_PATH)

        key = os.getenv(cls.ENV_KEY_NAME)
        if not key:
            key = Fernet.generate_key().decode()
            set_key(str(cls.ENV_PATH), cls.ENV_KEY_NAME, key)
        cls._fernet = Fernet(key.encode())

    @classmethod
    def encrypt(cls, text: str) -> str:
        if cls._fernet is None:
            cls._initialize()
        return cls._fernet.encrypt(text.encode()).decode()

    @classmethod
    def decrypt(cls, encrypted_text: str) -> str:
        if cls._fernet is None:
            cls._initialize()
        return cls._fernet.decrypt(encrypted_text.encode()).decode()