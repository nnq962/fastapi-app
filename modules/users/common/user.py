from enum import Enum

#------------------------------
# User Role
#------------------------------
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"