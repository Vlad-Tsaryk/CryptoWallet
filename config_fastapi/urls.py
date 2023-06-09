from fastapi import FastAPI

from src.auth.endpoints import auth_router
from src.users.endpoints import profile_router


def register_routers(app: FastAPI):
    """
    Register routers

    """
    app.include_router(profile_router, tags=["Profile"], prefix="/profile")

    app.include_router(auth_router, tags=["Auth"], prefix="/auth")
