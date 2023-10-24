from pydantic import DirectoryPath, EmailStr, field_validator, NewPath

from .base import AllowedApps, Base, ERole, NameStr, Username
from .config import SharedDir


class Name(Base):
    first: NameStr
    last: NameStr


class Extra(Base):
    allowed_apps: AllowedApps = []
    user_dir: DirectoryPath | NewPath | None = None
    shared_dirs: list[SharedDir] = []


class Account(Base):
    enabled: bool = True
    username: Username
    name: Name
    email: EmailStr
    role: ERole
    extra: Extra = Extra()


class Users(Base):
    accounts: list[Account]

    # noinspection PyNestedDecorators
    @field_validator("accounts")
    @classmethod
    def account_must_be_defined(cls, v: list[Account]) -> list[Account]:
        if len(v) == 0:
            raise ValueError("at least one account must be defined")

        return v

    # noinspection PyNestedDecorators
    @field_validator("accounts")
    @classmethod
    def username_must_be_unique(cls, v: list[Account]) -> list[Account]:
        usernames = list(map(lambda x: x.username, v))

        if len(usernames) != len(set(usernames)):
            raise ValueError("username must be unique")

        return v
