from typing import TYPE_CHECKING

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import UUID
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.schemas.account import AccountSchema
from src.schemas.user import CreateUserRequest, CreateUserSchemaAndEmailAndId, RequestChangeEmailSchema
from src.models.user import UserModel
from src.schemas.sign_up import SingUpSchema, SingUpCompleteSchema
from src.models.invite import InviteModel
from src.models.account import AccountModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode
from src.utils.generate_invite_code import generate_code
from src.utils.send_invite_code_to_mail import send_invite_code_to_email
import logging

if TYPE_CHECKING:
    from src.models.company import CompanyModel

from utils.hash_password import hash_password

logger = logging.getLogger(__name__)


class AccountService(BaseService):
    base_repository: str = "account"

    @transaction_mode
    async def checking_account_and_send_invitation(self, email: EmailStr) -> InviteModel:
        try:
            # Проверка существования аккаунта
            account_exist: bool = await self.uow.account.check_account_exist(email)

            if account_exist:
                logger.warning("Registration attempted with existing email: %s", email)
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already exists")

            code = generate_code()

            # Попытка добавить приглашение
            invite: InviteModel = await self.uow.invite.add_one_and_get_obj(email=email, code=code)

            # Отправка кода приглашения
            send_invite_code_to_email(email, code)
            logger.info("Invitation sent to: %s with code: %s", email, code)

        except IntegrityError:
            logger.warning("Duplicate key error for email %s. Invitation already exists.", email)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="This invitation has already been sent to the provided email.")

        except Exception:
            logger.exception("Ошибка при обработке приглашения для email %s", email)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

        else:
            return invite

    @transaction_mode
    async def check_invite_token(self, account: SingUpSchema) -> InviteModel:
        invite: InviteModel | None = await self.uow.invite.get_by_query_one_or_none(
            email=account.account_email,
            code=account.invite_token,
        )

        # Если приглашение не найдено, выбрасываем ошибку
        if invite is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite token.py not found or expired")

        return invite

    @transaction_mode
    async def register_company(self, sign_up_data: SingUpCompleteSchema) -> SingUpCompleteSchema:
        try:
            company: CompanyModel = await self.uow.company.add_one_and_get_obj(name=sign_up_data.company_name)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company with this name already exists.",
            )

        user: UserModel = await self._add_admin_user(sign_up_data.first_name, sign_up_data.last_name, company.id)

        account_new: AccountModel = await self._register_account(
            email=sign_up_data.account,
            password=sign_up_data.password,
            user_id=user.id,
            company_id=company.id,
        )

        return SingUpCompleteSchema(
            account=account_new.email,
            password=account_new.password,
            first_name=user.first_name,
            last_name=user.last_name,
            company_name=company.name,
        )

    async def _add_admin_user(self, first_name: str, last_name: str, company_id: UUID) -> UserModel:
        return await self.uow.user.add_one_and_get_obj(
            first_name=first_name,
            last_name=last_name,
            company_id=company_id,
            is_admin=True,
        )

    async def _register_account(
            self, email: EmailStr, password: str, user_id: int | str | UUID, company_id: UUID) -> AccountModel:
        hashed_password = hash_password(password)
        return await self.uow.account.add_one_and_get_obj(
            email=email,
            password=hashed_password,
            user_id=user_id,
            company_id=company_id,
        )

    @transaction_mode
    async def check_account_and_return_obj(
            self,
            email: EmailStr,
    ) -> AccountSchema | None:
        return await self.uow.account.get_by_query_one_or_none(email=email)

    @transaction_mode
    async def update_user_info(
            self,
            account: AccountSchema,
            new_data: CreateUserRequest,
    ) -> CreateUserSchemaAndEmailAndId:

        account: AccountModel | None = await self.uow.account.get_by_query_one_or_none(id=account.id)
        if not account:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization")
        user: UserModel | None = await self.uow.user.update_one_by_id(account.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

        user.first_name = new_data.first_name
        user.last_name = new_data.last_name
        user.middle_name = new_data.middle_name

        updated_user: UserModel = await self.uow.user.update_one_by_id(
            account.user_id, first_name=user.first_name, last_name=user.last_name, middle_name=user.middle_name,
        )
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return CreateUserSchemaAndEmailAndId(
            id=user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            middle_name=updated_user.middle_name,
            email=account.email,
        )

    @transaction_mode
    async def request_for_change_email(
        self,
        new_email: EmailStr,
        account: AccountSchema,
    ) -> RequestChangeEmailSchema:

        code = generate_code()
        invite_exist: bool = await self.uow.account.check_account_exist(new_email)
        if not invite_exist:
            await self.uow.invite.add_one(email=new_email, code=code)
            send_invite_code_to_email(new_email, code)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already exists")

        user_id = await self.uow.account.get_user_id_from_account(account.id)

        if not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User in not found")
        return RequestChangeEmailSchema(
            old_email=account.email,
            new_email=new_email,
            user_id=user_id,
        )

    @transaction_mode
    async def check_and_change_email(
            self,
            code: int,
            account: AccountSchema,
    ) -> RequestChangeEmailSchema:

        new_email: EmailStr = await self.uow.invite.get_email_from_code(code)
        if not new_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code is invalid")
        new_account: AccountModel = await self.uow.account.update_one_by_id(account.id, email=new_email)
        return RequestChangeEmailSchema(
            old_email=account.email,
            new_email=new_account.email,
            user_id=new_account.user_id,
        )
