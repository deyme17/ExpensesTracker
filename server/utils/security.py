import bcrypt
import base64
from jose import jwt
from datetime import datetime, timedelta

<<<<<<< HEAD
# 🔐 Секретний ключ для підпису токенів (в ідеалі зберігати в .env)
SECRET_KEY = "super_secret_key_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 години

# ✅ Хешування паролю з base64
=======
# 🔐 Ключ підпису токена
SECRET_KEY = "super_secret_key_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

>>>>>>> 9765729 (completed api)
def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return base64.b64encode(hashed).decode('utf-8')

<<<<<<< HEAD
# ✅ Перевірка паролю
=======
>>>>>>> 9765729 (completed api)
def verify_password(password: str, hashed: str) -> bool:
    hashed_bytes = base64.b64decode(hashed.encode('utf-8'))
    return bcrypt.checkpw(password.encode('utf-8'), hashed_bytes)

<<<<<<< HEAD
# 🎟 Створення access токена
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔓 Розшифрування токена
=======
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

>>>>>>> 9765729 (completed api)
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
