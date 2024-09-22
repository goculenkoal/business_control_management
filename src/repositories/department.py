from sqlalchemy import select, Result

from src.models.department.department import Department
from utils.repository import SqlAlchemyRepository


class DepartmentRepository(SqlAlchemyRepository):
    model = Department

    async def get_departament_id(self, departament_id: int) -> int | None:
        query = select(self.model.id).where(self.model.id == departament_id)
        departament_id: Result | None = await self.session.execute(query)
        return departament_id.scalar_one_or_none()
