from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from starlette.status import HTTP_201_CREATED
from utils.auth.admin import check_user_is_admin
from src.schemas.department.leader import AssignLeaderRequest, AssignLeaderResponse, LeaderResponse
from src.services.employee import EmployeeService
from src.schemas.department.employee import EmployeeCreateRequest, EmployeeResponse

from src.schemas.department.position import PositionCreateRequest, PositionResponse
from src.services.position import PositionService
from src.schemas.department.department import DepartmentCreateRequest, DepartmentCreateResponse
from src.services.department import DepartmentService
from src.services.company import CompanyService
from utils.auth.auth_utils import get_current_auth_active_account
from src.schemas.account import AccountSchema
if TYPE_CHECKING:
    from src.models.company import CompanyModel

router = APIRouter(prefix="/department", tags=["Department"])


@router.post(
    path="/create_department/",
    status_code=HTTP_201_CREATED,
)
async def create_department(
        department: DepartmentCreateRequest,
        account: AccountSchema = Depends(get_current_auth_active_account),
        service: DepartmentService = Depends(DepartmentService),
        company_service: CompanyService = Depends(CompanyService),
        is_admin: bool = Depends(check_user_is_admin),
) -> DepartmentCreateResponse:
    company_account: CompanyModel = await company_service.get_by_query_one_or_none(id=account.company_id)
    department = await service.create_department(department, company_account)
    return DepartmentCreateResponse(payload=department.__dict__)


@router.post(
    "/create_position",
    status_code=HTTP_201_CREATED,
)
async def create_position(
        position: PositionCreateRequest,
        account: AccountSchema = Depends(get_current_auth_active_account),
        department_service: DepartmentService = Depends(DepartmentService),
        position_service: PositionService = Depends(PositionService),
        is_admin: bool = Depends(check_user_is_admin),
) -> PositionResponse:
    created_position = await position_service.create_position(position, account, department_service)
    return PositionResponse(payload=created_position)


@router.post(
    "/create_employee",
    status_code=HTTP_201_CREATED,
)
async def create_employee(
        employee_data: EmployeeCreateRequest,
        account: AccountSchema = Depends(get_current_auth_active_account),
        department_service: DepartmentService = Depends(DepartmentService),
        employee_service: EmployeeService = Depends(EmployeeService),
        position_service: PositionService = Depends(PositionService),
        is_admin: bool = Depends(check_user_is_admin),
) -> EmployeeResponse:
    new_employee = await employee_service.create_new_employee(
        employee_data,
        account,
        department_service,
        position_service,
    )
    return EmployeeResponse(payload=new_employee.__dict__)


@router.post("/assign_leader")
async def assign_leader(
        request: AssignLeaderRequest,
        account: AccountSchema = Depends(get_current_auth_active_account),
        department_service: DepartmentService = Depends(DepartmentService),
        is_admin: bool = Depends(check_user_is_admin),
):
    create_leader: AssignLeaderResponse = await department_service.assign_leader(request, account)
    return LeaderResponse(payload=create_leader)
