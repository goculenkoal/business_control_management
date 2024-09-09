from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.invite import InviteDB
from src.models.base import BaseModel


class InviteModel(BaseModel):
    __tablename__ = "invite"

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    code: Mapped[int]

    def to_pydantic_schema(self) -> InviteDB:
        """Метод для преобразования в Pydantic модель."""
        return InviteDB(**self.__dict__)
