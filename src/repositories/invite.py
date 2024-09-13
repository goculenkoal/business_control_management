from pydantic import EmailStr
from sqlalchemy import select, Result

from src.models.invite import InviteModel
from src.utils.repository import SqlAlchemyRepository


class InviteRepository(SqlAlchemyRepository):
    model = InviteModel

    async def get_email_from_code(self, code: int) -> EmailStr:
        query = select(self.model.email).where(self.model.code == code)
        email: Result | None = await self.session.execute(query)
        return email.scalar_one_or_none()
