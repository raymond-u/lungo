import re
from ipaddress import IPv4Address
from typing import Any

from pydantic import AnyHttpUrl, field_validator

from .base import AppDirs, Base, PortType


class BaseSettings(Base):
    enabled: bool = True


class PluginConfig(Base):
    name: str
    descriptive_name: str | None = None
    version: str | None = None
    description: str | None = None

    compatible_with: str
    have_backend: bool
    backend_port: PortType | None = None
    require_account: bool

    web_path_name: str | None = None
    web_icon: str | None = None
    web_alt_icon: str | None = None

    @property
    def web_path(self) -> str:
        return self.web_path_name or self.name

    # noinspection PyNestedDecorators
    @field_validator("name")
    @classmethod
    def name_field_validator(cls, v: str) -> str:
        # Must be a valid file name
        if not re.fullmatch("[a-zA-Z0-9_-]+", v):
            raise ValueError("name must only contain alphanumeric characters, dash, or underscore")

        return v

    # noinspection PyNestedDecorators
    @field_validator("web_path_name")
    @classmethod
    def web_path_name_field_validator(cls, v: str | None) -> str | None:
        if v is None:
            return None

        # Must be a valid file name
        if not re.fullmatch("[a-zA-Z0-9_-]+", v):
            raise ValueError("web_path_name must only contain alphanumeric characters, dash, or underscore")

        return v


class PluginContext(Base):
    config: PluginConfig
    backend_base_url: AnyHttpUrl
    dirs: AppDirs
    ip_address: IPv4Address
    oathkeeper_url_regex: str
    web_base_url: AnyHttpUrl
    web_prefix: str
    custom: dict[str, Any]


class PluginOutput(Base):
    config: PluginConfig
    compose_services: str
    compose_secrets: str
    nginx_site: str
    oathkeeper_rules: str
    web_dependencies: list[str]
