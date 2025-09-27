# api/v1/schemas/users.py
from pydantic import BaseModel, EmailStr, Field
from modules.users.common.user import UserRole
from core.schemas import SuccessResponse

# -----------------------------
# Request Schemas
# -----------------------------
class UserCreate(BaseModel):
    """Schema cho request tạo user"""
    name: str = Field(..., min_length=10, max_length=255, example="Nguyễn Ngọc Quyết")
    phone: str = Field(..., pattern=r"^\d{10}$", example="0123456789")
    email: EmailStr | None = Field(None, example="nguyenngocquyet@gmail.com")
    position: str | None = Field(None, min_length=3, max_length=60, example="Dev IT")

# -----------------------------
# Data Schemas
# -----------------------------
class UserData(BaseModel):
    """User data trong response"""
    id: str
    name: str
    phone: str
    email: EmailStr | None
    position: str | None
    is_active: bool
    role: UserRole

# -----------------------------
# Response Schemas
# -----------------------------
class UserCreateResponse(SuccessResponse[UserData]):
    """Response cho tạo user"""
    pass

# -----------------------------
# Rebuild Schemas
# -----------------------------
UserCreate.model_rebuild()
UserData.model_rebuild()
UserCreateResponse.model_rebuild()