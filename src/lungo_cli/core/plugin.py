import sys
from abc import ABC
from importlib import import_module
from importlib.resources import as_file, files
from os import PathLike
from pathlib import Path
from typing import Any, ClassVar, final, Type

from aenum import extend_enum
from typer import Exit

from .console import Console
from .constants import PACKAGE_NAME
from .context import ContextManager
from .file import FileUtils
from .storage import Storage
from ..helpers.common import extract_multiline_value_from_yaml
from ..helpers.format import format_path, format_program
from ..models.base import EApp
from ..models.config import Plugins
from ..models.plugin import BaseSettings, Config, PluginOutput


class BasePlugin(ABC):
    """Base class for all plugins."""

    config: ClassVar[Config]

    custom: ClassVar[bool] = False
    installable: ClassVar[bool] = False
    installed: ClassVar[bool] = False
    alt_version: ClassVar[str | None] = None

    rendered: ClassVar[bool] = False

    def __init__(
        self,
        settings: BaseSettings,
        console: Console,
        context_manager: ContextManager,
        file_utils: FileUtils,
        storage: Storage,
    ):
        self.settings = settings
        self.console = console
        self.context_manager = context_manager
        self.file_utils = file_utils
        self.storage = storage

        self._output = None

    # Chaining `classmethod` descriptor with `property` descriptor is no longer supported
    # `ClassVar` parameter cannot include type variables
    @classmethod
    def get_plugin_settings_cls(cls) -> Type[BaseSettings]:
        return BaseSettings

    def get_render_context(self) -> dict[str, Any]:
        return {}

    def update_data(self) -> None: ...

    @classmethod
    @final
    def mark_as_rendered(cls) -> None:
        cls.rendered = True

    @property
    @final
    def output(self) -> PluginOutput:
        if self._output is None:
            if not self.rendered:
                self.console.print_error(f"Plugin {format_program(self.config.name)} has not been rendered.")
                raise Exit(code=1)

            plugin_dir = self.storage.installed_plugins_dir / self.config.name

            compose_content = self.file_utils.read_text(plugin_dir / "compose" / "compose.yaml", not_exist_ok=True)
            compose_services = extract_multiline_value_from_yaml(compose_content, "services")
            compose_secrets = extract_multiline_value_from_yaml(compose_content, "secrets")
            nginx_upstream = self.file_utils.read_text(plugin_dir / "nginx" / "upstream.conf", not_exist_ok=True)
            nginx_site = self.file_utils.read_text(plugin_dir / "nginx" / "site.conf", not_exist_ok=True)
            oathkeeper_rules = self.file_utils.read_text(
                plugin_dir / "oathkeeper" / "access_rules.yaml", not_exist_ok=True
            )
            web_dependencies = self.file_utils.read_text(
                plugin_dir / "web" / "dependencies.txt", not_exist_ok=True
            ).splitlines()

            self._output = PluginOutput(
                config=self.config,
                compose_services=compose_services,
                compose_secrets=compose_secrets,
                nginx_upstream=nginx_upstream,
                nginx_site=nginx_site,
                oathkeeper_rules=oathkeeper_rules,
                web_dependencies=web_dependencies,
            )

        return self._output


class PluginManager:
    """Manager for plugins."""

    def __init__(
        self,
        console: Console,
        context_manager: ContextManager,
        file_utils: FileUtils,
        storage: Storage,
    ):
        self.console = console
        self.context_manager = context_manager
        self.file_utils = file_utils
        self.storage = storage

        self._installable_plugin_classes = None
        self._installed_plugin_classes = None
        self._plugins = []

    @property
    def installable_plugin_classes(self) -> list[Type[BasePlugin]]:
        if self._installable_plugin_classes is None:
            self._installable_plugin_classes = self.import_builtin_plugins() + self.import_custom_plugins()

        return self._installable_plugin_classes

    @property
    def installed_plugin_classes(self) -> list[Type[BasePlugin]]:
        if self._installed_plugin_classes is None:
            self._installed_plugin_classes = self.import_installed_plugins()

        return self._installed_plugin_classes

    @property
    def plugins(self) -> list[BasePlugin]:
        return self._plugins

    def add_plugin(self, plugin_cls: Type[BasePlugin]) -> None:
        """Add a plugin to the application."""
        if not plugin_cls.installable:
            self.console.print_error(f"Plugin {format_program(plugin_cls.config.name)} is not installable.")
            raise Exit(code=1)

        dst = self.storage.installed_plugins_dir / plugin_cls.config.name

        if plugin_cls.custom:
            self.file_utils.copy(self.storage.custom_plugins_dir / plugin_cls.config.name, dst)
        else:
            self.file_utils.copy_package_resources(f"{PACKAGE_NAME}.plugins", plugin_cls.config.name, dst)

        plugin_cls.installed = True

    def remove_plugin(self, plugin_cls: Type[BasePlugin]) -> None:
        """Remove a plugin from the application."""
        if not plugin_cls.installed:
            self.console.print_error(f"Plugin {format_program(plugin_cls.config.name)} is not installed.")
            raise Exit(code=1)

        self.file_utils.remove(self.storage.installed_plugins_dir / plugin_cls.config.name)
        plugin_cls.installed = False

    def import_plugins(self, src: str | PathLike[str]) -> list[Type[BasePlugin]]:
        """Import plugins from the specified directory."""
        src = Path(src)

        if not src.is_dir():
            return []

        plugin_classes = []

        for plugin_dir in src.iterdir():
            if not plugin_dir.is_dir() or plugin_dir.name.startswith("_"):
                continue

            if not plugin_dir.joinpath("plugin.py").is_file():
                self.console.print_warning(f"Plugin at {format_path(plugin_dir)} does not seem to be valid. Skipping.")
                continue

            # Import modules with the same name from different directories
            try:
                sys.path.insert(0, str(plugin_dir))
                plugin_classes.append(import_module("plugin").Plugin)
            except Exception as e:
                self.console.print_warning(f"Failed to import plugin from {format_path(plugin_dir)} ({e}). Skipping.")
            finally:
                sys.modules.pop("plugin", None)
                sys.path.pop(0)

        return plugin_classes

    def import_builtin_plugins(self) -> list[Type[BasePlugin]]:
        """Import plugins from the built-in plugins directory."""
        with as_file(files(f"{PACKAGE_NAME}.plugins")) as package_dir:
            plugin_classes = self.import_plugins(package_dir)

            for plugin_cls in plugin_classes:
                plugin_cls.installable = True

            return plugin_classes

    def import_custom_plugins(self) -> list[Type[BasePlugin]]:
        """Import plugins from the custom plugins directory."""
        plugin_classes = self.import_plugins(self.storage.custom_plugins_dir)

        for plugin_cls in plugin_classes:
            plugin_cls.custom = True
            plugin_cls.installable = True

        return plugin_classes

    def import_installed_plugins(self) -> list[Type[BasePlugin]]:
        """Import installed plugins."""
        plugin_classes = self.import_plugins(self.storage.installed_plugins_dir)

        for plugin_cls in plugin_classes:
            plugin_cls.installed = True

        return plugin_classes

    def extend_models(self) -> None:
        """Extend the models with fields for installed plugins."""
        for plugin_cls in self.installed_plugin_classes:
            try:
                extend_enum(EApp, plugin_cls.config.name.upper(), plugin_cls.config.name)
                settings_cls = plugin_cls.get_plugin_settings_cls()
                Plugins.add_fields(**{plugin_cls.config.name: (settings_cls, settings_cls())})
            except Exception as e:
                self.console.print_warning(
                    f"Failed to load plugin {format_program(plugin_cls.config.name)} ({e}). Skipping."
                )
                continue

            self.console.print_debug(f"Loaded plugin {format_program(plugin_cls.config.name)}.")

    def initialize_plugins(self) -> None:
        """Initialize all plugins."""
        for plugin_cls in self.installed_plugin_classes:
            plugin_settings = getattr(self.context_manager.config.plugins, plugin_cls.config.name, None)

            if plugin_settings is None:
                self.console.print_error(f"Settings for plugin {format_program(plugin_cls.config.name)} are missing.")
                raise Exit(code=1)

            plugin = plugin_cls(plugin_settings, self.console, self.context_manager, self.file_utils, self.storage)
            self.plugins.append(plugin)
            self.context_manager.plugin_outputs.append(plugin.output)
