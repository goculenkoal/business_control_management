import uuid

from fastapi import HTTPException
from starlette import status

from src.schemas.account import AccountSchema
from src.schemas.user import CreateUserRequest, CreateUserSchemaAndEmail, CreateUserSchemaAndEmailAndId
from src.models.user import UserModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode
from src.utils.send_invite_code_to_mail import send_invite_token_link_email
from src.utils.token_create import create_invite_token


class UserService(BaseService):
    base_repository: str = "user"

    @transaction_mode
    async def create_user(self, user: CreateUserRequest) -> UserModel:
        """Create user."""
        return await self.uow.user.add_one_and_get_obj(**user.model_dump())

    @transaction_mode
    async def get_user_by_id(self, user_id: uuid) -> UserModel:
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing in the token.py payload.",
            )

        user = await self.uow.user.get_by_query_one_or_none(id=user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found.",
            )

        return user

    @transaction_mode
    async def add_one_user_for_company(
            self,
            employee: CreateUserSchemaAndEmail,
            account: AccountSchema,
    ) -> CreateUserSchemaAndEmailAndId:
        """CreateUserSchemaAndEmailAndId на вход: fast,last,middle name + email."""
        account__mail_exist: bool = await self.uow.account.check_account_exist(employee.email)
        if account__mail_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already exists")

        admin_user_id: uuid.UUID = await self.uow.account.get_user_id_from_account(account.id)
        is_admin: bool = await self.uow.user.check_if_user_is_admin(admin_user_id)
        print(admin_user_id)
        print(is_admin)
        if not is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create users")

        user: UserModel = await self.uow.user.add_one_and_get_obj(
            first_name=employee.first_name,
            last_name=employee.last_name,
            middle_name=employee.middle_name,
            company_id=account.company_id,
        )
        token = create_invite_token(user_id=user.id, company_id=account.company_id, employee_email=employee.email)
        print(f"token employee: {token}")
        send_invite_token_link_email(recipient_email=employee.email, code=token)

        return CreateUserSchemaAndEmailAndId(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            email=employee.email,
        )
