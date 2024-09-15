from pydantic import BaseModel, UUID4, EmailStr, ConfigDict, constr
from pydantic.v1 import validator

from src.schemas.base_response import BaseResponse


class AccountResponse(BaseModel):
    id: UUID4
    email: str


class CompanyAccountResponse(AccountResponse):
    company_id: UUID4


class ConfirmRegistrationResponse(BaseResponse):
    payload: CompanyAccountResponse
    detail: str


class IdAccountRequest(BaseModel):
    id: UUID4


class CreateAccountRequest(BaseModel):
    email: str
    password: str


class AccountSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    login_email: str
    password: str | None
    active: bool


class AccountUserSchema(BaseModel):
    login_email: EmailStr
    user_id: UUID4
    user_name: str | None = None
    user_last_name: str | None = None
    logged_in_at: float | None = None


class AccountInfoResponse(BaseResponse):
    payload: AccountUserSchema


class RequestPasswordCreate(BaseModel):
    password: constr(min_length=8)

    @classmethod
    @validator("password")
    def password_complexity(cls, password_value: str) -> str:
        missing_digit_error_message = "Пароль должен содержать хотя бы одну цифру"
        missing_letter_error_message = "Пароль должен содержать хотя бы одну букву"
        missing_special_char_error_message = "Пароль должен содержать хотя бы один специальный символ"
        if not any(char.isdigit() for char in password_value):
            raise ValueError(missing_digit_error_message)
        if not any(char.isalpha() for char in password_value):
            raise ValueError(missing_letter_error_message)
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/`~" for char in password_value):
            raise ValueError(missing_special_char_error_message)
        return password_value
