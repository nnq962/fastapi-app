import re
import unicodedata
from enum import Enum
from typing import Tuple

#------------------------------
# User Role
#------------------------------
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

#------------------------------
# Helper Functions
#------------------------------
def _normalize_name_part(part: str) -> str:
    """Normalize a name segment by stripping accents and non-alphanumerics."""
    cleaned = part.strip()
    if not cleaned:
        return ""

    cleaned = cleaned.replace("Đ", "D").replace("đ", "d")
    cleaned = unicodedata.normalize("NFD", cleaned)
    cleaned = "".join(ch for ch in cleaned if unicodedata.category(ch) != "Mn")
    cleaned = cleaned.lower()
    return re.sub(r"[^a-z0-9]", "", cleaned)

#------------------------------
# Generate Username and Email
#------------------------------
def generate_username_and_email(full_name: str, domain: str = "edulive.net") -> Tuple[str, str]:
    """Create username and email from a full name following the required pattern."""
    if not isinstance(full_name, str):
        raise TypeError("full_name must be a string")

    parts = [part for part in re.split(r"\s+", full_name.strip()) if part]
    if not parts:
        raise ValueError("full_name must contain at least one non-space character")

    first_name = _normalize_name_part(parts[-1])
    if not first_name:
        raise ValueError("Unable to derive first name from the provided full_name")

    initials = []
    for part in parts[:-1]:
        normalized = _normalize_name_part(part)
        if normalized:
            initials.append(normalized[0])

    username = first_name + "".join(initials)
    email = f"{username}@{domain}"
    return username, email