from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.models.base import BaseModel


class CompanyModel(BaseModel):
    __tablename__ = "company"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    inn: Mapped[str] = mapped_column(String, nullable=True)

    # Связь -> User
    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    accounts: Mapped[list["AccountModel"]] = relationship(
        "AccountModel",
        back_populates="company",
        cascade="all, delete-orphan",
    )
