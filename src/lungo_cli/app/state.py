from ..core.app import AppManager
from ..core.console import Console
from ..core.container import Container
from ..core.context import ContextManager
from ..core.database import AccountManager
from ..core.file import FileUtils
from ..core.network import HttpApiClient
from ..core.plugin import PluginManager
from ..core.renderer import Renderer
from ..core.storage import Storage

_console = Console()
_client = HttpApiClient(_console)
_file_utils = FileUtils(_console)
_storage = Storage(_console, _file_utils)
_context_manager = ContextManager(_console, _file_utils, _storage)
_container = Container(_console, _context_manager, _file_utils, _storage)
_renderer = Renderer(_console, _context_manager, _file_utils, _storage)
_plugin_manager = PluginManager(_console, _context_manager, _file_utils, _renderer, _storage)
_account_manager = AccountManager(_client, _console, _container, _file_utils, _storage)
_app_manager = AppManager(
    _account_manager, _console, _context_manager, _file_utils, _plugin_manager, _renderer, _storage
)


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


def renderer() -> Renderer:
    return _renderer


def plugin_manager() -> PluginManager:
    return _plugin_manager


def account_manager() -> AccountManager:
    return _account_manager


def app_manager() -> AppManager:
    return _app_manager
