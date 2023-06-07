from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .config import settings
from .users.router import router as user_router


# from app.api import router
# from app.core.config import settings
# from app.core.db import get_session
# from app.models import User
# from app.schemas.user import UserOut


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    application.include_router(user_router)
    return application


app = create_application()


# app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content = jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


# @app.get("/", response_model=list[UserOut])
# async def all_users(session: AsyncSession = Depends(get_session)):
#     result = await session.execute(select(User))
#     return result.scalars().all()
# new_user = User(email=user.email, password=user.password, username=user.username)
# session.add(new_user)
# await session.commit()

# async def root():
#     test()
#     # 'hash'
#     # 'from_address'
#     # 'to_address'
#     # 'value'
#     # 'receipt_status'
#     # 'gas_price'
#     # 'block_timestamp'
#
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# @app.get("/wallet/transaction-list/")
# async def transaction_list(address: str):
#     return {"message": address}
