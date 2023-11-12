from enum import Enum
from importlib import metadata
from os import PathLike
from pathlib import Path
from shutil import which

from ..core.constants import PACKAGE_NAME


def get_app_version() -> str:
    """Get the version of the app."""
    return metadata.version(PACKAGE_NAME)


def get_file_permissions(path: str | PathLike[str]) -> str:
    """Get the permissions of a file."""
    return oct(Path(path).stat().st_mode)[-3:]


def program_exists(program: str) -> bool:
    """Check if a program exists in the user's PATH."""
    return which(program) is not None


def is_in_enum(value: any, enum: type[Enum]) -> bool:
    """Check if a value is in an enum."""
    return any((item == value or item.value == value) for item in enum)
