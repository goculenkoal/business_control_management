from pydantic import BaseModel, UUID4


class AccountResponse(BaseModel):
    id: UUID4
    email: str


class IdAccountRequest(BaseModel):
    id: UUID4


class CreateAccountRequest(BaseModel):
    email: str
    password: str
