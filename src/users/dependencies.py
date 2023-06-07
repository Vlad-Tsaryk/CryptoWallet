from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_token_data
from src.database import get_session
from src.users.models import User
from src.users.schemas import UserRegistration
from .service import get_user_by_email

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    token_data = get_token_data(credentials.credentials)
    user = await session.get(User, token_data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def valid_user_create(
    user: UserRegistration, session: AsyncSession = Depends(get_session)
) -> UserRegistration:
    if await get_user_by_email(user.email, session):
        raise HTTPException(status_code=400, detail="Email is already taken.")
    return user
