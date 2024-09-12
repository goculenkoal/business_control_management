from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from starlette.status import HTTP_201_CREATED, HTTP_200_OK


from src.schemas.sign_up import SingUpSchema, SingUpCompleteSchema, SignUpCompleteResponse
from src.schemas.invite import CreateInviteResponse
from src.services.account import AccountService

if TYPE_CHECKING:
    from src.models.invite import InviteModel

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
