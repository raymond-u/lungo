from ..core.app import AppManager
from ..core.console import Console
from ..core.container import Container
from ..core.context import ContextManager
from ..core.database import AccountManager
from ..core.file import FileUtils
from ..core.network import HttpApiClient
from ..core.renderer import Renderer
from ..core.storage import Storage

_console = Console()
_file_utils = FileUtils(_console)
_storage = Storage(_console, _file_utils)
_context_manager = ContextManager(_console, _file_utils, _storage)
_container = Container(_console, _file_utils, _storage, _context_manager)
_account_manager = AccountManager(_console, _file_utils, _storage, HttpApiClient(_console), _container)
_renderer = Renderer(_console, _file_utils, _storage)
_app_manager = AppManager(_console, _file_utils, _storage, _context_manager, _account_manager, _renderer)


def console() -> Console:
    return _console


def file_utils() -> FileUtils:
    return _file_utils


def storage() -> Storage:
    return _storage


def context_manager() -> ContextManager:
    return _context_manager


def container() -> Container:
    return _container


def account_manager() -> AccountManager:
    return _account_manager


def renderer() -> Renderer:
    return _renderer


def app_manager() -> AppManager:
    return _app_manager
