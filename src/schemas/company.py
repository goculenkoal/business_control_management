from pydantic import BaseModel, EmailStr, Field


class CreateCompanyScheme(BaseModel):
    account: EmailStr = Field(max_length=50)
    password: str = Field(max_length=50)
