from fastapi import FastAPI

from ibay_service.broker import router


def create_application() -> FastAPI:
    application = FastAPI(title="Ibay_service", lifespan=router.lifespan_context)
    return application


app = create_application()
