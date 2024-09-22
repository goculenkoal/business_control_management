from pydantic import BaseModel, UUID4

from src.schemas.base_response import BaseCreateResponse


class DepartmentResponse(BaseModel):
    department_id: int
    parent_department_id: int | None = None
    department_name: str
    path: str
    company_id: UUID4


class DepartmentCreateRequest(BaseModel):
    name: str
    parent_department_id: int | None = None


class DepartmentCreateResponse(BaseCreateResponse):
    payload: DepartmentResponse
