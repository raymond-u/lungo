from typing import Self

from pydantic import DirectoryPath, EmailStr, field_validator, model_validator, NewPath

from .base import AllowedAppsType, Base, ERole, NameStrType, UsernameType
from .config import SharedDir


class Name(Base):
    first: NameStrType
    last: NameStrType


class Extra(Base):
    allowed_apps: AllowedAppsType = []
    user_dir: DirectoryPath | NewPath | None = None
    shared_dirs: list[SharedDir] = []


class Account(Base):
    enabled: bool = True
    username: UsernameType
    name: Name
    email: EmailStr
    role: ERole
    extra: Extra = Extra()

    @model_validator(mode="after")
    def account_model_validator(self) -> Self:
        # Anonymous account must have role `guest`
        if self.username == "anonymous" and self.role != ERole.GUEST:
            raise ValueError("anonymous account must have role guest")

        # `extra.allowed_apps` has no effect on anonymous account
        if self.username == "anonymous" and self.extra.allowed_apps:
            raise ValueError("anonymous account must have no allowed apps defined in the extra field")

        return self


class Users(Base):
    accounts: list[Account]

    # noinspection PyNestedDecorators
    @field_validator("accounts")
    @classmethod
    def accounts_field_validator(cls, v: list[Account]) -> list[Account]:
        # At least one account must be defined
        if len(v) == 0:
            raise ValueError("at least one account must be defined")

        # Username must be unique
        usernames = list(map(lambda x: x.username, v))
        if len(usernames) != len(set(usernames)):
            raise ValueError("username must be unique")

        # Email must be unique
        emails = list(map(lambda x: x.email, v))
        if len(emails) != len(set(emails)):
            raise ValueError("email must be unique")

        return v
