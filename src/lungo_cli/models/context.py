from ipaddress import IPv4Address

from pydantic import AnyHttpUrl

from .base import AppDirs, Base
from .config import Config
from .plugin import PluginOutput
from .users import Users


class Constants(Base):
    app_name: str
    app_name_capitalized: str
    architecture: str
    package_name: str
    openresty_version: str
    keto_version: str
    kratos_version: str
    oathkeeper_version: str
    node_version: str


class Context(Base):
    constants: Constants
    config: Config
    users: Users
    plugin_outputs: list[PluginOutput]
    app_dirs: AppDirs
    base_url: AnyHttpUrl
    dev: bool
    ip_addresses: dict[str, IPv4Address]
