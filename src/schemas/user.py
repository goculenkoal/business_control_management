from pydantic import BaseModel, UUID4, Field, ConfigDict, EmailStr

from src.schemas.base_response import BaseCreateResponse, BaseResponse


class UserID(BaseModel):
    id: UUID4


class CreateUserRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    middle_name: str | None = Field(max_length=50, default=None)


class CreateUserSchemaAndEmail(CreateUserRequest):
    email: EmailStr


class CreateUserSchemaAndEmailAndId(CreateUserSchemaAndEmail):
    id: UUID4


class UserInvitationResponse(BaseResponse):
    payload: CreateUserSchemaAndEmailAndId
    detail: str


class RequestChangeEmailSchema(BaseModel):
    old_email: EmailStr
    new_email: EmailStr
    user_id: UUID4


class ChangeEmailResponse(BaseResponse):
    payload: RequestChangeEmailSchema


class UserDB(UserID, CreateUserRequest):
    pass


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB


class UpdateUserResponse(CreateUserResponse):
    payload: CreateUserSchemaAndEmailAndId


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr | None
    is_active: bool = True
