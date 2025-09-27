# app/api/v1/routers/users.py
from fastapi import APIRouter, status
from modules.users.services.user import UserService
from core.exceptions import CustomHTTPException
from api.v1.schemas.users import (
    UserCreate, 
    UserCreateResponse, 
    UserData,
    UserResponseExamples
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "", 
    response_model=UserCreateResponse, 
    status_code=status.HTTP_201_CREATED,
    responses={
        400: UserResponseExamples.ERROR_400,
        422: UserResponseExamples.ERROR_422
    }
)
async def create_user(user_data: UserCreate):
    """
    Tạo user mới
    
    - **name**: Tên đầy đủ của user (10-255 ký tự)
    - **phone**: Số điện thoại (10 chữ số)
    - **email**: Email của user (optional)
    - **position**: Vị trí công việc (optional, 3-60 ký tự)
    
    **Responses:**
    - **201**: User được tạo thành công
    - **400**: User đã tồn tại
    - **422**: Dữ liệu không hợp lệ
    """
    # Check phone exists
    existing_phone = await UserService.get_user_by_phone(user_data.phone)
    if existing_phone:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="User already registered",
            error_code="USER_EXISTS",
            details=f"Phone number {user_data.phone} is already registered"
        )
    
    # Check email exists (if provided)
    if user_data.email:
        existing_email = await UserService.get_user_by_email(user_data.email)
        if existing_email:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User already registered",
                error_code="USER_EXISTS",
                details=f"Email {user_data.email} is already registered"
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