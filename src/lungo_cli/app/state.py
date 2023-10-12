from ..core.console import Console
from ..core.container import Container
from ..core.database import AccountManager
from ..core.network import HttpApiClient
from ..core.renderer import Renderer
from ..core.storage import Storage

_console = Console()
_storage = Storage(_console)
_container = Container(_console, _storage)
_account_manager = AccountManager(_console, _storage, HttpApiClient(_console), _container)
_renderer = Renderer(_console, _storage)


def console() -> Console:
    return _console


def storage() -> Storage:
    return _storage


def container() -> Container:
    return _container


def account_manager() -> AccountManager:
    return _account_manager


def renderer() -> Renderer:
    return _renderer
