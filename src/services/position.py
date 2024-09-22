from typing import TYPE_CHECKING

from fastapi import HTTPException
from src.schemas.account import AccountSchema
from src.services.department import DepartmentService
from src.schemas.department.position import PositionCreateRequest, PositionCreateResponse

from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

if TYPE_CHECKING:
    from src.models.department.postion import Position


class PositionService(BaseService):
    base_repository: str = "position"

    @transaction_mode
    async def create_position(
            self,
            position: PositionCreateRequest,
            account: AccountSchema,
            service: DepartmentService,
    ) -> PositionCreateResponse:
        department_exist: bool = await service.check_department_exist(position.department_id, account.company_id)
        if department_exist:
            position: Position = await self.uow.position.add_one_and_get_obj(**position.model_dump())
            return PositionCreateResponse(
                title=position.title,
                department_id=position.department_id,
            )
        raise HTTPException(status_code=404, detail="Department not found or not belonging to the company")

    @transaction_mode
    async def check_position_exist(self, position_id: int) -> bool:
        department = await self.uow.position.get_by_query_one_or_none(id=position_id)
        if department is None:
            raise HTTPException(status_code=404, detail="Position not found or not belonging to the department")

        return True
