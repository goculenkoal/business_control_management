import uuid

from fastapi import HTTPException
from starlette import status

from src.schemas.user import CreateUserRequest
from src.models.user import UserModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository: str = "user"

    @transaction_mode
    async def create_user(self, user: CreateUserRequest) -> UserModel:
        """Create user."""
        return await self.uow.user.add_one_and_get_obj(**user.model_dump())

    @transaction_mode
    async def get_user_by_id(self, user_id: uuid) -> UserModel:
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing in the token.py payload.",
            )

        user = await self.uow.user.get_by_query_one_or_none(id=user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found.",
            )

        return user
