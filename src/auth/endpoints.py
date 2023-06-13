from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.users import service as user_service
from src.users.schemas import UserLogin, UserRegistration
from .dependencies import create_access_token
from .schemas import Token
from .service import authenticate_user

auth_router = APIRouter()


@auth_router.post("/login/", response_model=Token)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(session, email=data.email, password=data.password)
    return {
        "access_token": create_access_token(user, not_expire=data.remember_me),
        "token_type": "bearer",
    }


@auth_router.post("/register/", response_model=Token)
async def register_user(
    new_user: UserRegistration,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    user = await user_service.create_user(new_user, session)
    background_tasks.add_task(user_service.send_register_message, user)
    return {"access_token": create_access_token(user), "token_type": "bearer"}
