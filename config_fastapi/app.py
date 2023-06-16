from fastapi import FastAPI, Request, status, Path
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import (
    JSONResponse,
    FileResponse,
    RedirectResponse,
    StreamingResponse,
)
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import (
    ObjectDoesNotExistError,
)
from sqlalchemy_file.storage import StorageManager

from config.config import settings
from config_fastapi.broker import router
from config_fastapi.urls import register_routers


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME, lifespan=router.lifespan_context)
    register_routers(application)
    return application


app = create_application()


@app.get("/media/{storage}/{file_id}", response_class=FileResponse, tags=["Media"])
async def serve_files(storage: str = Path(...), file_id: str = Path(...)):
    try:
        file = StorageManager.get_file(f"{storage}/{file_id}")
        if isinstance(file.object.driver, LocalStorageDriver):
            """If file is stored in local storage, just return a
            FileResponse with the fill full path."""
            return FileResponse(
                file.get_cdn_url(), media_type=file.content_type, filename=file.filename
            )
        elif file.get_cdn_url() is not None:
            """If file has public url, redirect to this url"""
            return RedirectResponse(file.get_cdn_url())
        else:
            """Otherwise, return a streaming response"""
            return StreamingResponse(
                file.object.as_stream(),
                media_type=file.content_type,
                headers={"Content-Disposition": f"attachment;filename={file.filename}"},
            )
    except ObjectDoesNotExistError:
        return JSONResponse({"detail": "Not found"}, status_code=404)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content = jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
