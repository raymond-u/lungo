import re
from ipaddress import IPv4Address
from typing import Any

from pydantic import AnyHttpUrl, field_validator

from .base import AppDirs, Base, PortType


class BaseSettings(Base):
    enabled: bool = True


class PluginManifest(Base):
    name: str
    """The name of the plugin. Must only contain alphanumeric characters, dash, or underscore."""
    version: str
    """The version of the plugin. Must be a valid semantic version."""
    descriptive_name: str | None = None
    """A human-readable name for the plugin. If not provided, it will be the same as the name."""
    description: str | None = None
    """A description of the plugin."""

    compatible_with: str
    """The version of Lungo that this plugin is compatible with. Must be a valid semantic version."""
    have_backend: bool
    """Whether the plugin requires a backend."""
    backend_host_ports: list[PortType] | None = None
    """The ports that the backend requires. If provided, they will be checked for availability."""
    backend_port: PortType | None = None
    """The port that the backend exposes to the web interface."""
    require_account: bool
    """Whether the plugin requires an account to be used. This determines if an anonymous account is needed."""

    web_path_name: str | None = None
    """The name of the slug for the web interface. If not provided, it will be the same as the name."""
    web_icon: str | None = None
    """The path to the icon for the web app. If not provided, it will be a default icon."""
    web_alt_icon: str | None = None
    """The path to the icon when highlighted for the web app. If not provided, it will be the same as the icon."""

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
    manifest: PluginManifest
    backend_base_url: AnyHttpUrl | None
    dirs: AppDirs
    ip_address: IPv4Address
    oathkeeper_url_regex: str
    web_base_url: AnyHttpUrl
    web_prefix: str
    custom: dict[str, Any]


class PluginOutput(Base):
    manifest: PluginManifest
    compose_services: str
    compose_secrets: str
    nginx_site: str
    oathkeeper_rules: str
    web_dependencies: list[str]
