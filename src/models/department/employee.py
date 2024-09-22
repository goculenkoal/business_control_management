from uuid import UUID

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.base import BaseModel


class Employee(BaseModel):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="employee", uselist=False)

    position_id: Mapped[int] = mapped_column(Integer, ForeignKey("positions.id"), nullable=True)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))

    position: Mapped["Position"] = relationship("Position", back_populates="employees")
    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="employees",
        foreign_keys=[department_id],
    )

    manager_id: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id"), nullable=True)
    manager: Mapped["Employee"] = relationship("Employee", remote_side=[id], back_populates="subordinates")

    subordinates: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="manager",
    )
    managed_departments: Mapped["Department"] = relationship(
        "Department",
        back_populates="leader",
        foreign_keys="Department.leader_id",
    )
