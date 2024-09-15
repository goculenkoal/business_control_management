from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from starlette.status import HTTP_201_CREATED, HTTP_200_OK


from src.services.account import AccountService
from src.api.v1.routers.auth_utils import get_current_auth_active_account
from src.schemas.account import AccountSchema, RequestPasswordCreate, ConfirmRegistrationResponse
from src.schemas.user import CreateUserRequest, CreateUserResponse, CreateUserSchemaAndEmailAndId, UpdateUserResponse, \
    RequestChangeEmailSchema, ChangeEmailResponse, CreateUserSchemaAndEmail, UserInvitationResponse
from src.services.user import UserService
from src.utils.token_create import get_user_id_from_token

if TYPE_CHECKING:
    from src.models.user import UserModel
    from src.models.account import AccountModel

router = APIRouter(prefix="/user")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
)
async def create_user(
        user: CreateUserRequest,
        service: UserService = Depends(UserService),
) -> CreateUserResponse:
    """Create user."""
    created_user: UserModel = await service.create_user(user)
    return CreateUserResponse(payload=created_user.to_pydantic_schema())


@router.put(
    path="/update_info",
    status_code=HTTP_200_OK,
)
async def change_info(
        new_data: CreateUserRequest,
        account: AccountSchema = Depends(get_current_auth_active_account),
        service: AccountService = Depends(AccountService),
) -> UpdateUserResponse:
    user: CreateUserSchemaAndEmailAndId = await service.update_user_info(account, new_data)
    return UpdateUserResponse(payload=user)


@router.post(
    path="/request_change_email",
    status_code=HTTP_200_OK,
)
async def request_for_change_email(
        email: EmailStr,
        account: AccountSchema = Depends(get_current_auth_active_account),
        service: AccountService = Depends(AccountService),
) -> ChangeEmailResponse:
    request_change_email: RequestChangeEmailSchema = await service.request_for_change_email(email, account)

    return ChangeEmailResponse(payload=request_change_email)


@router.post(
    path="/confirm_email",
    status_code=HTTP_200_OK,
)
async def confirm_email(
        code: int,
        service: AccountService = Depends(AccountService),
        account: AccountSchema = Depends(get_current_auth_active_account),

) -> ChangeEmailResponse:
    payload: RequestChangeEmailSchema = await service.check_and_change_email(code, account)

    return ChangeEmailResponse(payload=payload)


@router.post(
    path="/send_invite_new_user",
    status_code=HTTP_200_OK,
)
async def create_new_user(
        new_user: CreateUserSchemaAndEmail,
        account: AccountSchema = Depends(get_current_auth_active_account),
        service: UserService = Depends(UserService),
) -> UserInvitationResponse:
    """Создает нового сотрудника, и привязывает к компании,отправляет приглашение на почту."""
    user: CreateUserSchemaAndEmailAndId = await service.add_one_user_for_company(new_user, account)
    return UserInvitationResponse(
        payload=user,
        detail="Invitation token has been sent successfully.",
    )


@router.post("/confirm_registration/{invite_token}")
async def confirm_registration(
        invite_token: str,
        password: RequestPasswordCreate,
        service: AccountService = Depends(AccountService),
) -> ConfirmRegistrationResponse:
    user_id, employee_email, company_id = get_user_id_from_token(invite_token)
    account_new: AccountModel = await service.create_account(
        user_id,
        employee_email,
        password.password,
        company_id,
    )

    return ConfirmRegistrationResponse(
        payload=account_new.__dict__,
        detail="Password has been set successfully",
    )
