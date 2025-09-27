# modules/users/services/user.py
from typing import List, Optional
from modules.users.models.user import User


#------------------------------
# User Service
#------------------------------
class UserService:
    """User Service"""
    
    @staticmethod
    async def create_user(
        name: str,
        phone: str,
        email: Optional[str] = None,
        position: Optional[str] = None
    ) -> User:
        """Tạo user mới"""
        user = User(email=email, name=name, position=position, phone=phone)
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
    async def list_users() -> List[User]:
        """Lấy toàn bộ user"""
        return await User.find_all().to_list()