from src.schemas.schemas import CreateUserRequest
from src.models.user import UserModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository: str = "user"

    @transaction_mode
    async def create_user(self, user: CreateUserRequest) -> UserModel:
        """Create user."""
        return await self.uow.user.add_one_and_get_obj(**user.model_dump())
