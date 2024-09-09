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
        account = result.scalars().first()  # Извлекаем первую запись, если она существует
        return account is not None
