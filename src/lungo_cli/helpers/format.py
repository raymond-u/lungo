from enum import Enum
from os import PathLike


def format_command(*value: str) -> str:
    """Format a shell command for console output."""
    return f"[green]{' '.join(filter(None, value))}[/green]"


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


def format_input(value: int | str | Enum) -> str:
    """Format user input for console output."""
    if isinstance(value, Enum):
        return f"[cyan]{value.value}[/cyan]"
    else:
        return f"[cyan]{value}[/cyan]"
