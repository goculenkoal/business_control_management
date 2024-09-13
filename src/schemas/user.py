
from pydantic import BaseModel, UUID4, Field, ConfigDict, EmailStr

from src.schemas.base_response import BaseCreateResponse


class UserID(BaseModel):

    id: UUID4


class CreateUserRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    middle_name: str | None = Field(max_length=50, default=None)


class UserDB(UserID, CreateUserRequest):
    pass


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr | None
    is_active: bool = True
