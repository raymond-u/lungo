from ..core.console import Console
from ..core.container import Container
from ..core.database import FlatFile, UsersFile
from ..core.files import AppFiles

_app_files = AppFiles()
_console = Console()
_container = Container(_console, _app_files.compose_dir)
_flat_file = FlatFile(_console)
_users_file = UsersFile(_app_files, _console, _container)


def app_files() -> AppFiles:
    return _app_files


def console() -> Console:
    return _console


def container() -> Container:
    return _container


def flat_file() -> FlatFile:
    return _flat_file


def users_file() -> UsersFile:
    return _users_file
