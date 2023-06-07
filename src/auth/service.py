from typing import Optional

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.security import verify_password
from src.users.models import User
from src.users.service import get_user_by_email


async def authenticate_user(
    session: AsyncSession, email: EmailStr, password: str
) -> Optional[User]:
    user = await get_user_by_email(email, session)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or user not exist")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return user
