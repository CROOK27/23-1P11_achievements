import bcrypt
import jwt
from core.config import settings
from datetime import datetime, timedelta

def encode_jwt(
        payload: dict,
        privet_key: str = settings.auth_jwt.privet_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now+ timedelta(minutes=expire_minutes)
    to_encode.update(
        exp = expire,
        iat = now
    )
    encode = jwt.encode(
        to_encode,
        privet_key,
        algorithm = algorithm
    )
    return encode

def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    decode = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decode

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    hash = bcrypt.hashpw(pwd_bytes, salt)
    return hash
    

def validate_password(
        password: str,
        hashed_password: bytes
        ) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )
    