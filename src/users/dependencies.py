from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.users.schemas import UserRegistration
from .service import get_user_by_email


async def valid_user_create(
    user: UserRegistration, session: AsyncSession = Depends(get_session)
) -> UserRegistration:
    if await get_user_by_email(user.email, session):
        raise HTTPException(status_code=400, detail="Email is already taken.")
    return user
