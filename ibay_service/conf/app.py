from fastapi import FastAPI

from ibay_service.broker import router
from ibay_service.delivery import start_delivery_service


def create_application() -> FastAPI:
    application = FastAPI(title="Ibay_service", lifespan=router.lifespan_context)
    return application


@router.after_startup
async def start_delivery(app: FastAPI):
    await start_delivery_service()


app = create_application()
