import subprocess
from enum import Enum
from importlib import metadata
from os import PathLike
from shutil import which
from typing import Iterable

from ..core.constants import PACKAGE_NAME


def get_app_version() -> str:
    """Get the version of the app."""
    return metadata.version(PACKAGE_NAME)


def run_shell_command(
    *command: str, cwd: str | PathLike[str] | None = None, show_output: bool = False, umask: int = -1
):
    """Run a shell command."""
    command = list(filter(None, command))

    if show_output:
        subprocess.run(command, check=True, cwd=cwd, umask=umask)
    else:
        subprocess.run(command, check=True, cwd=cwd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, umask=umask)


def program_exists(program: str) -> bool:
    """Check if a program exists in the user's PATH."""
    return which(program) is not None


def format_command(value: str | Iterable[str]) -> str:
    """Format a shell command for console output."""
    if isinstance(value, str):
        return f"[green]{value}[/green]"

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


def format_input(value: str | Enum) -> str:
    """Format user input for console output."""
    if isinstance(value, Enum):
        return f"[cyan]{value.value}[/cyan]"
    else:
        return f"[cyan]{value}[/cyan]"
