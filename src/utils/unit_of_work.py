import functools
from abc import ABC, abstractmethod
from collections.abc import Callable, Awaitable
from types import TracebackType
from typing import Never, Any

from src.repositories.invite import InviteRepository
from src.repositories.account import AccountRepository
from src.databases.database import async_session_maker
from src.repositories.user import EmployeeRepository


class AbstractUnitOfWork(ABC):
    user: EmployeeRepository

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> Never:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions."""

    def __init__(self) -> None:

        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.user = EmployeeRepository(self.session)
        self.account = AccountRepository(self.session)
        self.invite = InviteRepository(self.session)

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


AsyncFunc = Callable[..., Awaitable[Any]]


def transaction_mode(func: AsyncFunc) -> AsyncFunc:
    """Decorate a function with transaction mode."""

    @functools.wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper
