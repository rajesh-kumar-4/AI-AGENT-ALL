from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .api import router
from .config import settings
from .exceptions import AppException
from .logging_config import logger
from .repository import TaskRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RaraphSOPVT application.")
    database_path = settings.database_url.replace("sqlite:///", "")
    TaskRepository(database_path)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="A sample RaraphSOPVT backend application with CRUD, security, logging and global exception handling.",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(router)

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning("Handled app exception: %s", exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"error": "internal_server_error", "message": "An unexpected error occurred."},
        )

    return app


app = create_app()
