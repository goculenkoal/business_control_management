from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException
from starlette import status

from schemas.account import AccountSchema
from src.services.user import UserService
from src.utils.auth.auth_utils import get_current_auth_active_account

if TYPE_CHECKING:
    from src.models.user import UserModel


async def check_user_is_admin(
        account: AccountSchema = Depends(get_current_auth_active_account),
        service: UserService = Depends(UserService),
) -> bool:
    """Проверка, является ли пользователь администратором по идентификатору аккаунта."""
    user: UserModel = await service.get_user_by_id(account.user_id)
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create users")
    return True
