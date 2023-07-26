from functools import wraps
from typing import ParamSpec, TypeVar, Callable

from config.database import async_session

P = ParamSpec("P")
R = TypeVar("R")


def add_session(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    async def wrapped(*args, **kwargs):
        async with async_session() as session:  # noqa
            return await func(session=session, *args, **kwargs)

    return wrapped
