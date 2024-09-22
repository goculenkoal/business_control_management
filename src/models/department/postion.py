from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.base import BaseModel


class Position(BaseModel):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id", ondelete="CASCADE"))

    department: Mapped["Department"] = relationship("Department", back_populates="positions")
    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="position")
