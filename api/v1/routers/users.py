# app/api/v1/routers/users.py
from fastapi import APIRouter, status
from modules.users.services.user import UserService
from core.exceptions import CustomHTTPException
from api.v1.schemas.users import UserCreate, UserCreateResponse, UserData

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """Tạo user mới"""
    existing = await UserService.get_user_by_phone(user_data.phone)
    if existing:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="User already registered",
            error_code="USER_EXISTS",
            details=f"Phone number {user_data.phone} is already registered"
        )
    
    user = await UserService.create_user(user_data.name, user_data.phone, user_data.email, user_data.position)
    
    return UserCreateResponse(
        message="User created successfully",
        data=UserData(
            id=str(user.id),
            name=user.name,
            phone=user.phone,
            email=user.email,
            position=user.position,
            is_active=user.is_active,
            role=user.role
        )
    )