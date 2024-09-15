import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException
from pydantic import EmailStr
from starlette import status

from src.config import settings

SECRET_KEY = settings.secret_key  # Замените на свой секретный ключ
ALGORITHM = "HS256"  # Алгоритм шифрования (можно использовать другой)
EXPIRATION_TIME_MINUTES = 15  # Время действия токена в минутах


def create_invite_token(user_id: uuid, company_id: uuid, employee_email: EmailStr) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME_MINUTES)
    expiration_timestamp = int(expiration.timestamp())

    token_data = {
        "s": str(user_id),
        "c": str(company_id),
        "m": str(employee_email),
        "exp": expiration_timestamp,
    }
    print(SECRET_KEY)
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_id_from_token(token: str) -> tuple[Any, Any, Any] | None:
    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("s")
        email_employee = payload.get("m")
        company_id = payload.get("c")
        if user_id:
            return user_id, email_employee, company_id
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
