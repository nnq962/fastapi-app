from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from core.config import settings
from core.mongo import lifespan
from core.exceptions import (
    custom_http_exception_handler, 
    validation_exception_handler,
    general_exception_handler,
    CustomHTTPException
)
from api import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
        swagger_ui_parameters={"tryItOutEnabled": True}
    )

    # Add global exception handlers
    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app

app = create_app()