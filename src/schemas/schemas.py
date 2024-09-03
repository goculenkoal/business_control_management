
from pydantic import BaseModel, UUID4, Field
from starlette.status import HTTP_201_CREATED, HTTP_200_OK


class UserID(BaseModel):

    id: UUID4


class CreateUserRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    middle_name: str | None = Field(max_length=50, default=None)


class UserDB(UserID, CreateUserRequest):
    pass


class BaseResponse(BaseModel):
    status: int = HTTP_200_OK
    error: bool = False


class BaseCreateResponse(BaseResponse):
    status: int = HTTP_201_CREATED
    error: bool = False


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB
