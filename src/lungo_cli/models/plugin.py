from .base import Base


class BaseSettings(Base):
    enabled: bool = True


class PluginConfig(Base):
    name: str
    descriptive_name: str | None = None
    version: str | None = None
    description: str | None = None

    compatible_with: str | None = None
    have_backend: bool
    require_account: bool

    web_icon: str | None = None
    web_alt_icon: str | None = None


class PluginOutput(Base):
    config: PluginConfig
    compose_services: str
    compose_secrets: str
    nginx_upstream: str
    nginx_site: str
    oathkeeper_rules: str
    web_dependencies: list[str]
