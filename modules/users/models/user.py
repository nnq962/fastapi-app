# modules/users/models/user.py
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from typing import Optional
from modules.users.common.user import UserRole

# -----------------------------
# User Model
# -----------------------------
class User(Document):
    # Thông tin tự thêm
    name: str
    phone: Indexed(str, unique=True)
    position: Optional[str] = None

    # Thông tin tự động tạo bởi hệ thống
    username: Indexed(str, unique=True)
    password: str = "123456"
    email: Indexed(EmailStr, unique=True)
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"  # tên collection trong MongoDB

# -----------------------------
# Rebuild Model
# -----------------------------
User.model_rebuild()