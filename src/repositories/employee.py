from src.models.department.employee import Employee
from src.utils.repository import SqlAlchemyRepository


class EmployeeRepository(SqlAlchemyRepository):
    model = Employee
