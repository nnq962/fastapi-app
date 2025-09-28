# app/api/v1/routers/users.py
from fastapi import APIRouter, Query, status
from modules.users.services.user import UserService
from core.exceptions import CustomHTTPException
from api.v1.schemas.users import (
    UserCreate,
    UserCreateResponse,
    UserData,
    UserCreateResponseExamples,
    UserListResponse,
    UserListResponseExamples,
)
from modules.users.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

# -----------------------------
# Create User
# -----------------------------
@router.post(
    "", 
    response_model=UserCreateResponse, 
    status_code=status.HTTP_201_CREATED,
    responses={
        400: UserCreateResponseExamples.ERROR_400,
        422: UserCreateResponseExamples.ERROR_422
    }
)
async def create_user(user_data: UserCreate):
    """
    Tạo user mới
    
    - **name: Tên đầy đủ của user (10-255 ký tự)
    - **phone**: Số điện thoại (10 chữ số)
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
        
    user = await UserService.create_user(user_data.name, user_data.phone, user_data.position)
    
    return UserCreateResponse(
        message="User created successfully",
        data=UserData(
            id=str(user.id),
            name=user.name,
            phone=user.phone,
            username=user.username,
            email=user.email,
            position=user.position,
            is_active=user.is_active,
            role=user.role
        )
    )

# -----------------------------
# Get Users
# -----------------------------
@router.get(
    "",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: UserListResponseExamples.ERROR_404,
    },
)
async def get_users(
    user_id: str | None = Query(default=None, alias="id"),
    username: str | None = Query(default=None, alias="user_name"),
):
    """Lấy user theo id/username hoặc toàn bộ danh sách nếu không truyền tham số."""

    def _to_user_data(user: User) -> UserData:
        return UserData(
            id=str(user.id),
            name=user.name,
            phone=user.phone,
            username=user.username,
            email=user.email,
            position=user.position,
            is_active=user.is_active,
            role=user.role,
        )

    if user_id:
        user = await UserService.get_user_by_id(user_id)
        if not user:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                error_code="USER_NOT_FOUND",
                details=f"User with id {user_id} was not found",
            )

        return UserListResponse(
            message="User retrieved successfully",
            data=[_to_user_data(user)],
        )

    if username:
        user = await UserService.get_user_by_username(username)
        if not user:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                error_code="USER_NOT_FOUND",
                details=f"User with username {username} was not found",
            )

        return UserListResponse(
            message="User retrieved successfully",
            data=[_to_user_data(user)],
        )

    users = await UserService.list_users()
    return UserListResponse(
        message="Users listed successfully",
        data=[_to_user_data(user) for user in users],
    )
