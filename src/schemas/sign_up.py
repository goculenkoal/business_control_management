from pydantic import BaseModel, Field, conint, EmailStr

from src.schemas.schemas import BaseCreateResponse


class SingUpSchema(BaseModel):
    account_email: EmailStr = Field(max_length=50)
    invite_token: conint(ge=100000, le=999999)


class SingUpCompleteSchema(BaseModel):
    account: EmailStr = Field(max_length=50)
    password: str = Field(max_length=128)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    company_name: str = Field(max_length=50)


class SignUpCompleteResponse(BaseCreateResponse):
    payload: SingUpCompleteSchema
