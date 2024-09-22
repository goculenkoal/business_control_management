from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

import utils.auth.utils
from utils.auth.auth_utils import (
    validate_auth_account,
    get_current_token_payload,
    get_current_auth_active_account,
)

from src.schemas.invite import CreateInviteResponse
from src.schemas.sign_up import SingUpCompleteSchema, SignUpCompleteResponse, SingUpSchema
from src.services.account import AccountService
from src.schemas.token import TokenInfo, TokenInfoResponse
from src.services.user import UserService

from src.schemas.account import AccountSchema, AccountUserSchema, AccountInfoResponse

if TYPE_CHECKING:
    from src.models.invite import InviteModel
    from src.models.user import UserModel

router = APIRouter(prefix="/auth/v1", tags=["Auth"])


@router.post(
    path="/sign-up-complete",
    status_code=HTTP_201_CREATED,
)
async def sign_up_complete(
        account: SingUpCompleteSchema,
        service: AccountService = Depends(AccountService),
) -> SignUpCompleteResponse:
    company_with_admin_user = await service.register_company(account)
    return SignUpCompleteResponse(payload=company_with_admin_user)


@router.get(
    path="/check_account/{account}",
    status_code=HTTP_201_CREATED,
)
async def register_check_account(
        email: EmailStr,
        service: AccountService = Depends(AccountService),
) -> CreateInviteResponse:
    """Проверяет наличие почты в базе.

    если она не обнаружена,
    генерирует проверочный код, добавляет информацию
    в приглашения, отправляет приглашение на почту.
    """
    invite: InviteModel = await service.checking_account_and_send_invitation(email)

    return CreateInviteResponse(payload=invite.to_pydantic_schema())


@router.post(
    path="/sign-up",
    status_code=HTTP_200_OK,
)
async def sign_up(
        account: SingUpSchema,
        service: AccountService = Depends(AccountService),

) -> CreateInviteResponse:
    """на вход схема: мейл и инвайт, чекаем в БД мейл и инвайт возвращаем InviteResponse."""
    sign_up_account = await service.check_invite_token(account)

    return CreateInviteResponse(payload=sign_up_account.to_pydantic_schema())


@router.post(
    path="/login",
    status_code=HTTP_200_OK,
)
async def auth_account_jwt(
        account: AccountSchema = Depends(validate_auth_account),
) -> TokenInfoResponse:
    jwt_payload = {
        "sub": account.email,
        "username": account.email,
        "user_id": str(account.user_id),
    }
    token = utils.auth.utils.encode_jwt(jwt_payload)
    token_info = TokenInfo(access_token=token)

    return TokenInfoResponse(payload=token_info)


@router.get(
    path="/users/me/",
    status_code=HTTP_200_OK,
)
async def auth_user_check_self_info(
        account: AccountSchema = Depends(get_current_auth_active_account),
        service: UserService = Depends(UserService),
        payload: dict = Depends(get_current_token_payload),
) -> AccountInfoResponse:
    user_id = payload.get("user_id")
    user: UserModel = await service.get_user_by_id(user_id)

    iat = payload.get("iat")
    account_info = AccountUserSchema(
        login_email=account.email,
        user_id=account.user_id,
        user_name=user.first_name,
        user_last_name=user.last_name,
        logged_in_at=iat,
    )

    return AccountInfoResponse(
        payload=account_info,
    )
