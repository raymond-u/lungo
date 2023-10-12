from pydantic import DirectoryPath, EmailStr, NewPath

from .base import AllowedApps, Base, ERole, Username


class Name(Base):
    first: str
    last: str


class Extra(Base):
    allowed_apps: AllowedApps = []
    user_dir: DirectoryPath | NewPath | None = None


class Account(Base):
    enabled: bool = True
    username: Username
    name: Name
    email: EmailStr
    role: ERole
    extra: Extra = Extra()


class Users(Base):
    accounts: list[Account]
