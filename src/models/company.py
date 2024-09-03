from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class CompanyModel(BaseModel):
    __tablename__ = "company"

    company_name: Mapped[str] = mapped_column(String(50))
    inn: Mapped[int]
