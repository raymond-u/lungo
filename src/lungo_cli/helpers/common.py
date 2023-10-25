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


def format_command(*value: str) -> str:
    """Format a shell command for console output."""
    return f"[green]{' '.join(value)}[/green]"


def format_program(value: str) -> str:
    """Format a program name for console output."""
    return f"[cyan]{value}[/cyan]"


def format_section(value: str) -> str:
    """Format a command section for console output."""
    return f"[turquoise2]{value}[/turquoise2]"


def format_path(value: str | PathLike[str]) -> str:
    """Format a path for console output."""
    return f"[magenta]{value}[/magenta]"


def format_link(value: str, title: str | None = None) -> str:
    """Format a link for console output."""
    if title:
        return f"[link={value}]{title}[/link]"
    else:
        return f"[link={value}]{format_path(value)}[/link]"


def format_input(value: str | Enum) -> str:
    """Format user input for console output."""
    if isinstance(value, Enum):
        return f"[cyan]{value.value}[/cyan]"
    else:
        return f"[cyan]{value}[/cyan]"


def is_in_enum(value: any, enum: type[Enum]) -> bool:
    """Check if a value is in an enum."""
    return any((item == value or item.value == value) for item in enum)
