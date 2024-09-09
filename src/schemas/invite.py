from datetime import datetime

from pydantic import UUID4, BaseModel

from src.schemas.schemas import BaseCreateResponse


class InviteId(BaseModel):
    id: UUID4


class InviteDB(InviteId):
    email: str
    code: int
    created_at: datetime


class CreateInviteResponse(BaseCreateResponse):
    payload: InviteDB
