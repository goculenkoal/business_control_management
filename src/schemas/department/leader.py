from pydantic import BaseModel

from src.schemas.base_response import BaseResponse


class AssignLeaderRequest(BaseModel):
    department_id: int
    leader_id: int


class AssignLeaderResponse(BaseModel):
    department_id: int
    leader_id: int


class LeaderResponse(BaseResponse):
    payload: AssignLeaderResponse
