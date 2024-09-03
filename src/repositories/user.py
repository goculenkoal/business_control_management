from src.models.user import UserModel
from src.utils.repository import SqlAlchemyRepository


class EmployeeRepository(SqlAlchemyRepository):
    """класс для работы репозитория чз модель."""

    model = UserModel
