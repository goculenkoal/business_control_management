import uuid

from sqlalchemy import select, Result

from src.models.company import CompanyModel
from utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = CompanyModel

    async def get_company_id(self, account_company_id: uuid) -> uuid:
        query = select(self.model.id).where(self.model.id == account_company_id)
        company_id: Result | None = await self.session.execute(query)
        return company_id.scalar_one_or_none()
