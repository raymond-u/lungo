import sys
from abc import ABC
from importlib import import_module
from importlib.resources import as_file, files
from os import PathLike
from pathlib import Path
from typing import Any, ClassVar, final

from aenum import extend_enum
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from pydantic.fields import FieldInfo
from typer import Exit

from .console import Console
from .constants import PACKAGE_NAME
from .context import ContextManager
from .file import FileUtils
from .storage import Storage
from ..helpers.common import extract_multiline_value_from_yaml, get_app_version
from ..helpers.format import format_path, format_program
from ..models.base import EApp
from ..models.config import Config, Plugins, Privilege, Privileges, Rules
from ..models.context import Context
from ..models.plugin import BaseSettings, PluginConfig, PluginOutput
from ..models.users import Account, Extra, Users


class BasePlugin[T: BaseSettings](ABC):
    """Base class for all plugins."""

    config: ClassVar[PluginConfig]

    custom: ClassVar[bool] = False
    installable: ClassVar[bool] = False
    installed: ClassVar[bool] = False
    compatible: ClassVar[bool] = True
    alt_version: ClassVar[str | None] = None

    rendered: ClassVar[bool] = False

    def __init__(
        self,
        settings: T,
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
    def get_plugin_settings_cls(cls) -> type[T]:
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

        self._builtin_plugin_classes = None
        self._custom_plugin_classes = None
        self._installable_plugin_classes = None
        self._installed_plugin_classes = None
        self._compatible_plugin_classes = None
        self._plugins = []

    @property
    def builtin_plugin_classes(self) -> list[type[BasePlugin]]:
        if self._builtin_plugin_classes is None:
            with as_file(files(f"{PACKAGE_NAME}.plugins")) as package_dir:
                plugin_classes = self.import_plugins(package_dir)

                for plugin_cls in plugin_classes:
                    plugin_cls.installable = True

                self._builtin_plugin_classes = plugin_classes

        return self._builtin_plugin_classes

    @property
    def custom_plugin_classes(self) -> list[type[BasePlugin]]:
        if self._custom_plugin_classes is None:
            plugin_classes = self.import_plugins(self.storage.custom_plugins_dir)

            for plugin_cls in plugin_classes:
                plugin_cls.custom = True
                plugin_cls.installable = True

            self._custom_plugin_classes = plugin_classes

        return self._custom_plugin_classes

    @property
    def installable_plugin_classes(self) -> list[type[BasePlugin]]:
        if self._installable_plugin_classes is None:
            self._installable_plugin_classes = self.builtin_plugin_classes + self.custom_plugin_classes

        return self._installable_plugin_classes

    @property
    def installed_plugin_classes(self) -> list[type[BasePlugin]]:
        if self._installed_plugin_classes is None:
            plugin_classes = self.import_plugins(self.storage.installed_plugins_dir)

            for plugin_cls in plugin_classes:
                plugin_cls.installed = True

            self._installed_plugin_classes = plugin_classes

        return self._installed_plugin_classes

    @property
    def compatible_plugin_classes(self) -> list[type[BasePlugin]]:
        if self._compatible_plugin_classes is None:
            self._compatible_plugin_classes = [
                plugin_cls for plugin_cls in self.installed_plugin_classes if plugin_cls.compatible
            ]

        return self._compatible_plugin_classes

    @property
    def plugins(self) -> list[BasePlugin]:
        return self._plugins

    def add_plugin(self, plugin_cls: type[BasePlugin]) -> bool:
        """Add a plugin to the application."""
        if not plugin_cls.installable:
            self.console.print_warning(
                f"Plugin {format_program(plugin_cls.config.name)} is not installable. Skipping it."
            )
            return False

        dst = self.storage.installed_plugins_dir / plugin_cls.config.name

        if plugin_cls.custom:
            self.file_utils.copy(self.storage.custom_plugins_dir / plugin_cls.config.name, dst)
        else:
            self.file_utils.copy_package_resources(f"{PACKAGE_NAME}.plugins", plugin_cls.config.name, dst)

        plugin_cls.installed = True
        return True

    def remove_plugin(self, plugin_cls: type[BasePlugin]) -> bool:
        """Remove a plugin from the application."""
        if not plugin_cls.installed:
            self.console.print_warning(
                f"Plugin {format_program(plugin_cls.config.name)} is not installed. Skipping it."
            )
            return False

        self.file_utils.remove(self.storage.installed_plugins_dir / plugin_cls.config.name)

        plugin_cls.installed = False
        return True

    def import_plugins(self, src: str | PathLike[str]) -> list[type[BasePlugin]]:
        """Import plugins from the specified directory."""
        src = Path(src)

        if not src.is_dir():
            return []

        plugin_classes = []

        for plugin_dir in src.iterdir():
            if not plugin_dir.is_dir() or plugin_dir.name.startswith("_") or plugin_dir.name.startswith("."):
                continue

            if not plugin_dir.joinpath("plugin.py").is_file():
                self.console.print_warning(
                    f"Plugin at {format_path(plugin_dir)} does not seem to be valid. Skipping it."
                )
                continue

            # Import modules with the same name from different directories
            try:
                sys.path.insert(0, str(plugin_dir))

                plugin_cls = import_module("plugin").Plugin

                if plugin_cls.config.compatible_with:
                    plugin_version = plugin_cls.config.version

                    try:
                        if get_app_version() not in SpecifierSet(plugin_cls.config.compatible_with):
                            self.console.print_warning(
                                f"Plugin {format_program(plugin_cls.config.name)} "
                                f"{f'version {plugin_version}' if plugin_version else 'with an unknown version'} "
                                "is not compatible with the current version of the application. Skipping it."
                            )

                            plugin_cls.compatible = False
                    except InvalidSpecifier:
                        self.console.print_warning(
                            f"Plugin {format_program(plugin_cls.config.name)} "
                            f"{f'version {plugin_version}' if plugin_version else 'with an unknown version'} "
                            "has an invalid version specifier. Skipping it."
                        )

                        plugin_cls.compatible = False

                plugin_classes.append(plugin_cls)
            except Exception as e:
                self.console.print_warning(
                    f"Failed to import plugin from {format_path(plugin_dir)} ({e}). Skipping it."
                )
            finally:
                sys.modules.pop("plugin", None)
                sys.path.pop(0)

        return plugin_classes

    def extend_models(self) -> None:
        """Extend the models with fields for installed plugins."""
        for plugin_cls in self.compatible_plugin_classes:
            try:
                extend_enum(EApp, plugin_cls.config.name.upper(), plugin_cls.config.name)

                settings_cls = plugin_cls.get_plugin_settings_cls()
                field_info = FieldInfo(annotation=settings_cls, default=settings_cls())
                Plugins.model_fields[plugin_cls.config.name] = field_info
            except Exception as e:
                self.console.print_warning(
                    f"Failed to load plugin {format_program(plugin_cls.config.name)} ({e}). Skipping it."
                )
                continue

        Plugins.model_rebuild(force=True)
        Privilege.model_rebuild(force=True)
        Privileges.model_rebuild(force=True)
        Rules.model_rebuild(force=True)
        Config.model_rebuild(force=True)
        Extra.model_rebuild(force=True)
        Account.model_rebuild(force=True)
        Users.model_rebuild(force=True)
        Context.model_rebuild(force=True)

    def initialize_plugins(self) -> None:
        """Initialize all plugins."""
        for plugin_cls in self.compatible_plugin_classes:
            plugin_settings = getattr(self.context_manager.config.plugins, plugin_cls.config.name, None)

            if plugin_settings is None:
                self.console.print_error(f"Settings for plugin {format_program(plugin_cls.config.name)} are missing.")
                raise Exit(code=1)

            plugin = plugin_cls(plugin_settings, self.console, self.context_manager, self.file_utils, self.storage)
            plugin.update_data()
            self.plugins.append(plugin)
            self.console.print_debug(f"Loaded plugin {format_program(plugin.config.name)}.")
