from dataclasses import dataclass
from enum import Enum


class UserRole(Enum, str):
    """User role."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


@dataclass
class User:
    """User information."""
    username: str
    full_name: str
    email: str
    user_role: UserRole
    user_disabled: bool = False
    password: str = ...
