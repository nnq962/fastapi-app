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
        email: str, 
        position: str
    ) -> User:
        """Tạo user mới"""
        user = User(email=email, name=name, position=position, phone=phone)
        return await user.insert()

    @staticmethod
    async def get_user_by_phone(phone: str) -> User:
        """Lấy user theo số điện thoại"""
        return await User.find_one(User.phone == phone)