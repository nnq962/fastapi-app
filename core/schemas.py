# core/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Any, Optional, TypeVar, Generic

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """Global API response format"""
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[dict] = Field(default=None, exclude=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SuccessResponse(ApiResponse[T]):
    """Success response template"""
    success: bool = True

class ErrorResponse(ApiResponse[None]):
    """Error response template"""
    success: bool = False
    data: None = None

# Rebuild schemas
ApiResponse.model_rebuild()
SuccessResponse.model_rebuild()
ErrorResponse.model_rebuild()