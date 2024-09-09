

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


from src.schemas.account import AccountResponse
from src.models.base import BaseModel


class AccountModel(BaseModel):
    __tablename__ = "account"

    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)

    def to_pydantic_schema(self) -> AccountResponse:
        """Метод для преобразования в Pydantic модель."""
        return AccountResponse(
            id=self.id,
            email=self.email,

        )
