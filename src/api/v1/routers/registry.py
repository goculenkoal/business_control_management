from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from starlette import status
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.schemas.sign_up import SingUpSchema
from src.schemas.invite import CreateInviteResponse
from src.schemas.account import AccountResponse, CreateAccountRequest
from src.services.account import AccountService

if TYPE_CHECKING:
    from src.models.invite import InviteModel

router = APIRouter(prefix="/auth/v1", tags=["Auth"])


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


@router.get(
    path="/{account_id}",
    status_code=HTTP_200_OK,
)
async def find_account_by_id(
        account_id: UUID,
        service: AccountService = Depends(AccountService),
) -> AccountResponse:
    """Find account."""
    account = await service.check_id_account(account_id)  # Передаем ID в вашу модель запроса

    if not account:  # Проверяем, существует ли аккаунт
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return account.to_pydantic_schema()


@router.post(
    path="/register",
    status_code=HTTP_201_CREATED,
)
async def create_account(
        account: CreateAccountRequest,
        service: AccountService = Depends(AccountService),
) -> AccountResponse:
    create_account_new = await service.create_account(account)
    return AccountResponse(
        id=create_account_new.id,
        email=create_account_new.email,
    )
