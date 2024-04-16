from ipaddress import IPv4Address

from pydantic import AnyHttpUrl

from .base import AppDirs, Base
from .config import Config
from .plugin import PluginOutput
from .users import Users


class Constants(Base):
    app_name: str
    app_name_capitalized: str
    package_name: str


class Context(Base):
    constants: Constants
    config: Config
    users: Users
    plugin_outputs: list[PluginOutput]
    app_dirs: AppDirs
    base_url: AnyHttpUrl
    dev: bool
    ip_addresses: dict[str, IPv4Address]
