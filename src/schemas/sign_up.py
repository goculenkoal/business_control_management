from pydantic import BaseModel, Field, conint, EmailStr


class SingUpSchema(BaseModel):
    account_email: EmailStr = Field(max_length=50)
    invite_token: conint(ge=100000, le=999999)
