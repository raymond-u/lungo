from ipaddress import IPv4Address

from pydantic import AnyHttpUrl

from .base import Base
from .config import Config
from .plugin import PluginOutput
from .users import Users


class AppDirs(Base):
    cache_dir: str
    generated_dir: str
    managed_dir: str
    plugin_dir: str


class Context(Base):
    config: Config
    users: Users
    plugin_outputs: list[PluginOutput]
    app_dirs: AppDirs
    base_url: AnyHttpUrl
    dev: bool
    ip_addresses: dict[str, IPv4Address]
