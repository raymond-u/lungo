import socket
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


def port_is_available(port: int) -> bool:
    """Check if a port is available on the local machine."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0
