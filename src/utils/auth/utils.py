from datetime import timedelta, datetime, timezone
from typing import Any

import bcrypt
import jwt

from src.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> bytes:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)  # Используем timezone-aware datetime  now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire.timestamp(),  # Добавляем экспирацию в формате timestamp без timestamp
        iat=now.timestamp(),  # Добавляем время создания в формате timestamp
    )

    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )


def decoded_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
) -> dict[str, Any]:
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hash_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hash_password,
    )
