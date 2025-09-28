# app/api/v1/routers/users.py
from fastapi import APIRouter, Query, status
from pymongo.errors import DuplicateKeyError
from modules.users.services.user import UserService
from core.exceptions import CustomHTTPException
from api.v1.schemas.users import (
    UserCreate,
    UserCreateResponse,
    UserData,
    UserCreateResponseExamples,
    UserListResponse,
    UserListResponseExamples,
    UserDeleteResponse,
    UserDeleteResponseExamples,
)
from modules.users.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

# -----------------------------
# Helper Functions
# -----------------------------
def _to_user_data(user: User) -> UserData:
    """Chuyển đổi user thành UserData"""
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


def _duplicate_fields(error: DuplicateKeyError) -> set[str]:
    """Trích xuất danh sách field trùng từ DuplicateKeyError."""
    details = getattr(error, "details", None) or {}
    key_pattern = details.get("keyPattern") if isinstance(details, dict) else None

    if isinstance(key_pattern, dict):
        return {str(key) for key in key_pattern.keys()}

    message = str(error)
    known_fields = {"phone", "username", "email"}
    return {field for field in known_fields if field in message}

# -----------------------------
# Create User
# -----------------------------
@router.post(
    "", 
    response_model=UserCreateResponse, 
    status_code=status.HTTP_201_CREATED,
    responses={
        400: UserCreateResponseExamples.ERROR_400,
        409: UserCreateResponseExamples.ERROR_409,
        422: UserCreateResponseExamples.ERROR_422,
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
        
    try:
        user = await UserService.create_user(user_data.name, user_data.phone, user_data.position)
    except DuplicateKeyError as exc:
        duplicate_fields = _duplicate_fields(exc)

        if "phone" in duplicate_fields:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User already registered",
                error_code="USER_EXISTS",
                details=f"Phone number {user_data.phone} is already registered",
            )

        if duplicate_fields & {"username", "email"}:
            raise CustomHTTPException(
                status_code=status.HTTP_409_CONFLICT,
                message="Unable to generate unique username/email",
                error_code="USER_USERNAME_CONFLICT",
                details="Generated username/email already exists. Please retry the request.",
            )

        raise

    return UserCreateResponse(
        message="User created successfully",
        data=_to_user_data(user),
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

    users = await UserService.get_list_users()
    return UserListResponse(
        message="Users listed successfully",
        data=[_to_user_data(user) for user in users],
    )


# -----------------------------
# Delete User
# -----------------------------
@router.delete(
    "",
    response_model=UserDeleteResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: UserDeleteResponseExamples.ERROR_400,
        404: UserDeleteResponseExamples.ERROR_404,
    },
)
async def delete_user(
    user_id: str | None = Query(default=None, alias="id"),
    username: str | None = Query(default=None, alias="user_name"),
):
    """Xóa user theo id hoặc username."""

    if not user_id and not username:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Request must include id or user_name",
            error_code="USER_IDENTIFIER_REQUIRED",
            details="Provide either id or user_name to delete a user",
        )

    user: User | None
    if user_id:
        user = await UserService.get_user_by_id(user_id)
        identifier_detail = f"id {user_id}"
    else:
        assert username is not None  # for type checkers
        user = await UserService.get_user_by_username(username)
        identifier_detail = f"username {username}"

    if not user:
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="User not found",
            error_code="USER_NOT_FOUND",
            details=f"User with {identifier_detail} was not found",
        )

    await UserService.delete_user(user)

    return UserDeleteResponse(
        message="User deleted successfully",
    )
