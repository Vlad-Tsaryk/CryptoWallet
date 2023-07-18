from fastapi import FastAPI

from src.auth.endpoints import auth_router
from src.ibay.endpoints import ibay_router
from src.users.endpoints import profile_router
from src.wallet.endpoints import wallet_router


def register_routers(app: FastAPI):
    """
    Register routers
    """
    app.include_router(profile_router, tags=["Profile"], prefix="/profile")
    app.include_router(auth_router, tags=["Auth"], prefix="/auth")
    app.include_router(wallet_router, tags=["Wallets"], prefix="/wallets")
    app.include_router(ibay_router, tags=["Ibay"], prefix="/ibay")
