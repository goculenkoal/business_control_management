from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.account import AccountResponse
from src.models.base import BaseModel


class AccountModel(BaseModel):
    __tablename__ = "account"

    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    # Связь -> UserModel
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="account", uselist=False)

    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=True)
    company: Mapped["CompanyModel"] = relationship("CompanyModel", back_populates="accounts")

    def to_pydantic_schema(self) -> AccountResponse:
        """Метод для преобразования в Pydantic модель."""
        return AccountResponse(
            id=self.id,
            email=self.email,

        )
