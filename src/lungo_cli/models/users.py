from pydantic import DirectoryPath, EmailStr, NewPath

from .base import AllowedApps, Base, ERole, NameStr, Username


class Name(Base):
    first: NameStr
    last: NameStr


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
