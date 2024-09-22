from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import LtreeType
from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.department.employee import Employee


class Department(BaseModel):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    path: Mapped[str] = mapped_column(LtreeType, nullable=False)

    parent_department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="CASCADE"), nullable=True)

    positions: Mapped["Position"] = relationship("Position", back_populates="department")
    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=True)
    company: Mapped["CompanyModel"] = relationship("CompanyModel", back_populates="departments")
    parent_department: Mapped["Department"] = relationship(
        "Department",
        remote_side=[id],
        back_populates="subdepartments",
    )
    subdepartments: Mapped["Department"] = relationship(
        "Department",
        back_populates="parent_department",
        cascade="all, delete-orphan")
    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="department",
        foreign_keys="Employee.department_id",
    )

    leader_id: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id"), nullable=True)
    leader: Mapped["Employee"] = relationship(
        "Employee",
        foreign_keys=[leader_id],
        back_populates="managed_departments",
    )
