# core/exceptions.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from core.schemas import ErrorResponse
from datetime import datetime, timezone

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str, error_code: str = None, details: str = None):
        error_response = ErrorResponse(
            message=message,
            error={
                "code": error_code or "UNKNOWN_ERROR",
                "details": details or message
            }
        )
        super().__init__(status_code=status_code, detail=error_response.model_dump(mode='json'))

async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_response = ErrorResponse(
        message="Validation error",
        error={
            "code": "VALIDATION_ERROR",
            "details": exc.errors()
        }
    )
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump(mode='json')
    )

async def general_exception_handler(request: Request, exc: Exception):
    error_response = ErrorResponse(
        message="Internal server error",
        error={
            "code": "INTERNAL_ERROR",
            "details": str(exc)
        }
    )
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(mode='json')
    )