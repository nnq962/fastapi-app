# modules/users/services/user.py
from typing import List, Optional, Tuple
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
from modules.users.models.user import User
from modules.users.common.user import generate_username_and_email

# -----------------------------
# User Service
# -----------------------------
class UserService:
    """User Service"""
    
    @staticmethod
    async def create_user(
        name: str,
        phone: str,
        position: Optional[str] = None
    ) -> User:
        """Tạo user mới"""
        max_attempts = 20
        last_error: DuplicateKeyError | None = None

        for _ in range(max_attempts):
            username, email = await UserService._generate_unique_username_and_email(name)

            user = User(
                name=name,
                position=position,
                phone=phone,
                username=username,
                email=email,
            )

            try:
                return await user.insert()
            except DuplicateKeyError as exc:
                last_error = exc

                if UserService._is_duplicate_on_fields(exc, {"phone"}):
                    raise

                if not UserService._is_duplicate_on_fields(exc, {"username", "email"}):
                    raise

                # Khi trùng username/email, retry sinh giá trị mới.
                continue

        if last_error is not None:
            raise last_error

        raise RuntimeError("Failed to create user due to unexpected duplicate handling state")

    @staticmethod
    async def get_user_by_phone(phone: str) -> Optional[User]:
        """Lấy user theo số điện thoại"""
        return await User.find_one(User.phone == phone)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Lấy user theo email"""
        return await User.find_one(User.email == email)

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Lấy user theo username"""
        return await User.find_one(User.username == username)
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Lấy user theo id"""
        try:
            object_id = ObjectId(user_id)
        except (InvalidId, TypeError):
            return None

        return await User.get(object_id)
    
    @staticmethod
    async def get_list_users() -> List[User]:
        """Lấy toàn bộ user"""
        return await User.find_all().to_list()

    @staticmethod
    async def _generate_unique_username_and_email(full_name: str) -> Tuple[str, str]:
        """Tạo username/email duy nhất bằng cách thêm hậu tố số khi cần."""
        base_username, base_email = generate_username_and_email(full_name)
        domain = base_email.split("@", 1)[1]

        username = base_username
        suffix = 0

        while await User.find_one(User.username == username):
            suffix += 1
            username = f"{base_username}{suffix}"

        email = f"{username}@{domain}"
        return username, email

    @staticmethod
    async def delete_user(user: User) -> None:
        """Xóa user khỏi hệ thống."""
        await user.delete()

    @staticmethod
    def _is_duplicate_on_fields(error: DuplicateKeyError, fields: set[str]) -> bool:
        """Kiểm tra DuplicateKeyError có trùng với các field đã cho không."""
        details = getattr(error, "details", None) or {}
        key_pattern = details.get("keyPattern") if isinstance(details, dict) else None

        if isinstance(key_pattern, dict):
            duplicate_fields = {str(key) for key in key_pattern.keys()}
            if duplicate_fields & fields:
                return True

        message = str(error)
        return any(field in message for field in fields)
