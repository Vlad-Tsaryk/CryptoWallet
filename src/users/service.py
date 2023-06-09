from fastapi_mail import MessageSchema, MessageType, FastMail
from loguru import logger
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import email_conf
from src.users.models import User
from src.users.schemas import UserRegistration, UserUpdate


async def create_user(user: UserRegistration, session: AsyncSession) -> User:
    new_user = User(
        email=user.email,
        password=user.password,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    logger.success(f"User id-{new_user.id} successfully registered")
    return new_user


async def send_register_message(user: User) -> None:
    # send message to user email
    message = MessageSchema(
        subject="Crypto Wallet",
        recipients=[
            user.email,
        ],
        body=f"Hello, {user.first_name} {user.last_name}. Welcome to Crypto Wallet",
        subtype=MessageType.plain,
    )
    fm = FastMail(email_conf)
    await fm.send_message(message)


async def get_user_by_email(email: EmailStr, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def update_user(
    user: UserUpdate, current_user: User, session: AsyncSession
) -> User:
    user_data = user.dict(exclude_unset=True)

    for key, value in user_data.items():
        setattr(current_user, key, value)

    await session.commit()
    await session.refresh(current_user)
    logger.success(f"User id-{current_user.id} updated")

    return current_user
