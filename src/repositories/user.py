import uuid

from sqlalchemy import select

from src.models.user import UserModel
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    """класс для работы репозитория чз модель."""

    model = UserModel

    async def check_if_user_is_admin(self, user_id: uuid) -> bool:
        query = select(self.model.id).where(
            self.model.id == user_id,
            self.model.is_admin,
        )
        result = await self.session.execute(query)
        return result.scalars().first() is not None
