from pydantic import BaseModel, UUID4, EmailStr, ConfigDict

from src.schemas.base_response import BaseResponse


class AccountResponse(BaseModel):
    id: UUID4
    email: str


class IdAccountRequest(BaseModel):
    id: UUID4


class CreateAccountRequest(BaseModel):
    email: str
    password: str


class AccountSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    login_email: str
    password: str
    active: bool


class AccountUserSchema(BaseModel):
    login_email: EmailStr
    user_id: UUID4
    user_name: str | None = None  # Может быть пустым, если не предоставлено
    user_last_name: str | None = None  # Может быть пустым, если не предоставлено
    logged_in_at: float | None = None


class AccountInfoResponse(BaseResponse):
    payload: AccountUserSchema
