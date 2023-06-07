from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Form, UploadFile, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import create_access_token
from src.auth.schemas import Token
from src.auth.service import authenticate_user
from src.database import get_session
from src.users import service as user_service
from src.users.dependencies import get_current_user
from src.users.models import User
from src.users.schemas import UserRegistration, UserLogin, UserResponse, UserUpdate
from src.users.service import send_register_message

router = APIRouter(tags=["Users"])


@router.post("/register", response_model=Token)
async def register_user(
    new_user: UserRegistration,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    user = await user_service.create_user(new_user, session)
    background_tasks.add_task(send_register_message, user)
    return {"access_token": create_access_token(user), "token_type": "bearer"}


@router.post("/login/", response_model=Token)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(session, email=data.email, password=data.password)
    return {
        "access_token": create_access_token(user, not_expire=data.remember_me),
        "token_type": "bearer",
    }


@router.get("/profile/", response_model=UserResponse)
async def profile(user: User = Depends(get_current_user)):
    return user


@router.put("/profile/", response_model=UserResponse)
async def profile_update(
    username: Annotated[str, Form()],
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    profile_image: Optional[UploadFile] = None,
    password: str | None = Form(default=None),
    password_repeat: str | None = Form(default=None),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # validate form
    try:
        user = UserUpdate(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            password_repeat=password_repeat,
            profile_image=profile_image,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    return await user_service.update_user(user, current_user, session)
