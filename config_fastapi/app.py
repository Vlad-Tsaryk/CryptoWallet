from fastapi import FastAPI, Request, Path
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
from pydantic import ValidationError
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
async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    errors = []
    for each in exc.errors():
        result = {
            "code": "validation-error",
            "type": each.get("type"),
            "field": each.get("loc")[1],
            "message": each.get("msg"),
        }
        errors.append(result)

    return JSONResponse({"detail": errors}, status_code=422)
