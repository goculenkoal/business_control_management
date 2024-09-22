from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.account import AccountModel


class CompanyModel(BaseModel):
    __tablename__ = "company"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    inn: Mapped[str] = mapped_column(String, nullable=True)

    departments: Mapped[list["Department"]] = relationship("Department", back_populates="company")
    # Связь -> User
    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        back_populates="company",
    )

    accounts: Mapped[list["AccountModel"]] = relationship(
        "AccountModel",
        back_populates="company",
    )
