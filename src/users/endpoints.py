from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, UploadFile, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from src.dependencies import get_current_user
from src.users import service as user_service
from src.users.models import User
from src.users.schemas import UserResponse, UserUpdate

profile_router = APIRouter()


@profile_router.get("/", response_model=UserResponse)
async def profile(user: User = Depends(get_current_user)):
    return user


@profile_router.put("/", response_model=UserResponse)
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
