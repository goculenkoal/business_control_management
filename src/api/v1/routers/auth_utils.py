from typing import Any

from fastapi import Depends, Form, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from pydantic import EmailStr
from starlette import status

import auth.utils
from schemas.account import AccountSchema
from services.account import AccountService
from utils.hash_password import check_password


async def validate_auth_account(
        service: AccountService = Depends(AccountService),
        login_email: EmailStr = Form(),
        password: str = Form(),
) -> AccountSchema:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    account: AccountSchema | None = await service.check_account_and_return_obj(login_email)
    if not account:
        raise unauthed_exc
    if not check_password(
            hashed_password=account.password,
            original_password=password,
    ):
        raise unauthed_exc

    return account


http_bearer = HTTPBearer()


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict[str, Any]:
    token = credentials.credentials
    try:
        payload = auth.utils.decoded_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token.py error: {e}",
        )
    return payload


async def get_current_auth_account(
        payload: dict = Depends(get_current_token_payload),
        service: AccountService = Depends(AccountService),
) -> AccountSchema:
    account_email: str | None = payload.get("sub")
    account: AccountSchema | None = await service.check_account_and_return_obj(account_email)
    if account:
        return account
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token.py invalid",
    )


def get_current_auth_active_account(
        account: AccountSchema = Depends(get_current_auth_account),
) -> AccountSchema:
    if account.active:
        return account
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="user inactive")
