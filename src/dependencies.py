from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from propan import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import async_session
from config_fastapi.broker import broker
from src.auth.dependencies import get_token_data
from src.users.models import User

security = HTTPBearer()


async def get_session() -> AsyncSession:
    async with async_session() as session:  # noqa
        yield session


def get_broker() -> RabbitBroker:
    return broker


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
