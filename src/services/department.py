import asyncio
import uuid
from collections.abc import Sequence
from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy_utils import Ltree
from starlette import status

from src.schemas.department.leader import AssignLeaderRequest, AssignLeaderResponse
from src.schemas.account import AccountSchema
from src.models.department.employee import Employee
from src.models.company import CompanyModel

from src.schemas.department.department import DepartmentResponse, DepartmentCreateRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

if TYPE_CHECKING:
    from src.models.department.department import Department


class DepartmentService(BaseService):
    base_repository: str = "department"

    @transaction_mode
    async def create_department(
            self,
            department: DepartmentCreateRequest,
            company_account: CompanyModel,
    ) -> DepartmentResponse:
        if department.parent_department_id is not None:
            parent_department = await self.uow.department.get_by_query_one_or_none(id=department.parent_department_id)

            if not parent_department:
                raise HTTPException(status_code=404, detail="Parent department not found")

            path = Ltree(f'{parent_department.path}.{department.name.replace(" ", "_")}')
        else:
            path = Ltree(f'{company_account.name}.{department.name.replace(" ", "_")}')

        new_department: Department = await self.uow.department.add_one_and_get_obj(
            name=department.name,
            path=path,
            company_id=company_account.id,
            parent_department_id=department.parent_department_id,
        )

        return DepartmentResponse(
            department_id=new_department.id,
            department_name=new_department.name,
            path=str(new_department.path),
            parent_department_id=new_department.parent_department_id,
            company_id=new_department.company_id,
        )

    @transaction_mode
    async def check_department_exist(self, department_id: int, company_id: uuid) -> bool:

        department = await self.uow.department.get_by_query_one_or_none(id=department_id)

        if department is None:
            raise HTTPException(status_code=404, detail="Department not found")

        if department.company_id != company_id:
            raise HTTPException(status_code=403, detail="Unauthorized to create position for this department")
        return True

    @transaction_mode
    async def assign_leader(
            self,
            request: AssignLeaderRequest,
            account: AccountSchema,
    ) -> AssignLeaderResponse:
        department_exist: bool = await self.check_department_exist(
            request.department_id,
            account.company_id,
        )
        if not department_exist:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found.",
            )

        department: Department = await self.uow.department.get_by_query_one_or_none(id=request.department_id)
        if department.leader_id is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Leader is already assigned to the department.")
        department_update: Department = await self.uow.department.update_one_by_id(
            department.id,
            leader_id=request.leader_id)

        employees = await self._get_employees_by_department_id(department_update.id)
        await self._bulk_update_employees(employees, request.leader_id)
        return AssignLeaderResponse(department_id=department_update.id, leader_id=department_update.leader_id)

    async def _get_employees_by_department_id(self, department_id: int) -> Sequence[Employee]:
        return await self.uow.employee.get_by_query_all(department_id=department_id)

    async def _bulk_update_employees(self, employees: Sequence[Employee], leader_id: int) -> None:
        """Массовое обновление сотрудников."""
        non_leader_employees = [employee for employee in employees if employee.id != leader_id]

        update_tasks = [
            self.uow.employee.update_one_by_id(employee.id, manager_id=leader_id)
            for employee in non_leader_employees
        ]
        await asyncio.gather(*update_tasks)
