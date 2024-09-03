from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.schemas import UserDB
from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(50), default=None)

    def to_pydantic_schema(self) -> UserDB:
        return UserDB(**self.__dict__)
