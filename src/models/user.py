from uuid import UUID

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.schemas import UserDB
from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(50), default=None)

    is_user: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Внешний ключ, ссылающийся на компанию
    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id"), nullable=True)
    # Связь -> модель Company
    company: Mapped["CompanyModel"] = relationship("CompanyModel", back_populates="users")

    account: Mapped["AccountModel"] = relationship("AccountModel", back_populates="user", uselist=False)

    def to_pydantic_schema(self) -> UserDB:
        return UserDB(**self.__dict__)
