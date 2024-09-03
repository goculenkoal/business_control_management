from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED


from src.schemas.schemas import CreateUserRequest, CreateUserResponse
from src.services.user import UserService

if TYPE_CHECKING:
    from src.models.user import UserModel

router = APIRouter(prefix="/user")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
)
async def create_user(
        user: CreateUserRequest,
        service: UserService = Depends(UserService),
) -> CreateUserResponse:
    """Create user."""
    created_user: UserModel = await service.create_user(user)
    return CreateUserResponse(payload=created_user.to_pydantic_schema())
