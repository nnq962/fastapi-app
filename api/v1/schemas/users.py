# api/v1/schemas/users.py
from pydantic import BaseModel, EmailStr, Field
from modules.users.common.user import UserRole
from core.schemas import SuccessResponse, ErrorResponse

# -----------------------------
# Request Schemas
# -----------------------------
class UserCreate(BaseModel):
    """Schema cho request tạo user"""
    name: str = Field(..., min_length=10, max_length=255, example="Nguyễn Ngọc Quyết")
    phone: str = Field(..., pattern=r"^\d{10}$", example="0123456789")
    position: str | None = Field(None, min_length=3, max_length=60, example="Dev IT")

# -----------------------------
# Data Schemas
# -----------------------------
class UserData(BaseModel):
    """User data trong response"""
    id: str
    name: str
    phone: str
    position: str | None
    username: str
    email: EmailStr
    is_active: bool
    role: UserRole

# -----------------------------
# Create Response Schemas
# -----------------------------
class UserCreateResponse(SuccessResponse[UserData]):
    """Response cho tạo user"""
    pass

# -----------------------------
# Create Response Examples
# -----------------------------
class UserCreateResponseExamples:
    """Response examples cho create user"""
    
    SUCCESS_201 = {
        "description": "User created successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "User created successfully",
                    "data": {
                        "id": "68d8106764888819afe47f30",
                        "name": "Nguyễn Ngọc Quyết",
                        "phone": "0123456789",
                        "username": "quyetnn",
                        "email": "quyetnn@edulive.net",
                        "position": "Dev IT",
                        "is_active": True,
                        "role": "user"
                    },
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            }
        }
    }
    
    ERROR_400 = {
        "model": ErrorResponse,
        "description": "User already exists",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "message": "User already registered",
                    "error": {
                        "code": "USER_EXISTS",
                        "details": "Phone number 0123456789 is already registered"
                    },
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            }
        }
    }
    
    ERROR_422 = {
        "model": ErrorResponse,
        "description": "Validation error",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "message": "Validation error",
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "details": [
                            {
                                "loc": ["body", "phone"],
                                "msg": "string does not match regex",
                                "type": "value_error.str.regex"
                            }
                        ]
                    },
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            }
        }
    }

# -----------------------------
# List Response Schemas
# -----------------------------
class UserListResponse(SuccessResponse[list[UserData]]):
    """Response cho danh sách user"""
    pass

# -----------------------------
# List Response Examples
# -----------------------------
class UserListResponseExamples:
    """Response examples cho lấy user"""

    SUCCESS_200 = {
        "description": "Users listed successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Users listed successfully",
                    "data": [
                        {
                            "id": "68d8106764888819afe47f30",
                            "name": "Nguyễn Ngọc Quyết",
                            "phone": "0123456789",
                            "username": "quyetnn",
                            "email": "quyetnn@edulive.net",
                            "position": "Dev IT",
                            "is_active": True,
                            "role": "user"
                        }
                    ],
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            }
        }
    }

    ERROR_404 = {
        "model": ErrorResponse,
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "message": "User not found",
                    "error": {
                        "code": "USER_NOT_FOUND",
                        "details": "User with username johndoe was not found"
                    },
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            }
        }
    }

# -----------------------------
# Rebuild Schemas
# -----------------------------
UserCreate.model_rebuild()
UserData.model_rebuild()
UserCreateResponse.model_rebuild()
UserListResponse.model_rebuild()
