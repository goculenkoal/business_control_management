from pydantic import BaseModel, UUID4

from src.schemas.base_response import BaseCreateResponse


class EmployeeCreateRequest(BaseModel):
    name: str
    user_id: UUID4
    position_id: int
    department_id: int


class EmployeeCreateResponse(BaseModel):
    name: str
    user_id: UUID4
    position_id: int
    department_id: int


class EmployeeResponse(BaseCreateResponse):
    payload: EmployeeCreateResponse
