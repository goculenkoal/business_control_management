import uuid

from pydantic import EmailStr
from sqlalchemy import Result, select

from src.models.account import AccountModel
from src.utils.repository import SqlAlchemyRepository


class AccountRepository(SqlAlchemyRepository):
    """класс для работы репозитория чз модель."""

    model = AccountModel

    async def check_account_exist(self, email: EmailStr) -> bool:
        query = (
            select(self.model)
            .filter(self.model.email == email)
        )
        result: Result = await self.session.execute(query)
        account = result.scalars().first()
        return account is not None

    async def get_user_id_from_account(self, account_user_id: uuid) -> uuid:
        query = select(self.model.user_id).where(self.model.id == account_user_id)
        user_id: Result | None = await self.session.execute(query)
        return user_id.scalar_one_or_none()
