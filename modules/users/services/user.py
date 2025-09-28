# modules/users/services/user.py
from typing import List, Optional, Tuple
from bson import ObjectId
from bson.errors import InvalidId
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
        username, email = await UserService._generate_unique_username_and_email(name)

        user = User(name=name, position=position, phone=phone, username=username, email=email)
        return await user.insert()

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
