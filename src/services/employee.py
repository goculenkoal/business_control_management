from fastapi import HTTPException
from src.services.position import PositionService
from src.services.department import DepartmentService
from src.schemas.account import AccountSchema
from src.schemas.department.employee import EmployeeCreateRequest, EmployeeCreateResponse
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class EmployeeService(BaseService):
    base_repository: str = "employee"

    @transaction_mode
    async def create_new_employee(
            self,
            employee_data: EmployeeCreateRequest,
            account: AccountSchema,
            department_service: DepartmentService,
            position_service: PositionService,
    ) -> EmployeeCreateResponse:
        department_exist: bool = await department_service.check_department_exist(
            employee_data.department_id,
            account.company_id,
        )
        position_exist: bool = await position_service.check_position_exist(
            employee_data.position_id,
        )
        if department_exist & position_exist:
            return await self.uow.employee.add_one_and_get_obj(
                name=employee_data.name,
                user_id=employee_data.user_id,
                position_id=employee_data.position_id,
                department_id=employee_data.department_id,
            )

        raise HTTPException(status_code=401, detail="Smt wrong")
