from fastapi import HTTPException
from pydantic import UUID4, EmailStr
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.schemas.sign_up import SingUpSchema
from src.models.invite import InviteModel
from src.schemas.account import CreateAccountRequest
from src.models.account import AccountModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode
from src.utils.generate_invite_code import generate_code
from src.utils.send_invite_code_to_mail import send_invite_code_to_email
import logging

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

            # Генерация кода приглашения
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
    async def create_account(self, account: CreateAccountRequest) -> AccountModel:
        """Create Account."""
        return await self.uow.account.add_one_and_get_obj(**account.model_dump())

    @transaction_mode
    async def check_id_account(self, account_id: UUID4) -> AccountModel:
        """Create user."""
        return await self.uow.account.get_by_query_one_or_none(id=account_id)

    @transaction_mode
    async def check_invite_token(self, account: SingUpSchema) -> InviteModel:
        invite: InviteModel | None = await self.uow.invite.get_by_query_one_or_none(
            email=account.account_email,
            code=account.invite_token,
        )

        # Если приглашение не найдено, выбрасываем ошибку
        if invite is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite token not found or expired")

        return invite
