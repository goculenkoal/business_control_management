from pydantic import BaseModel

from src.schemas.base_response import BaseCreateResponse


class PositionCreateRequest(BaseModel):
    title: str
    department_id: int


class PositionCreateResponse(BaseModel):
    title: str
    department_id: int


class PositionResponse(BaseCreateResponse):
    payload: PositionCreateResponse


class PositionCreateRequest1111(BaseModel):
    department_id: int
