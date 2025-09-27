# modules/users/models/user.py
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from modules.users.common.user import UserRole

#------------------------------
# User Model
#------------------------------
class User(Document):
    name: str
    phone: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    position: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"  # tên collection trong MongoDB

#------------------------------
# Rebuild Model
#------------------------------
User.model_rebuild()