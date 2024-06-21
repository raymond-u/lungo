import os
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
from .constants import PACKAGE_NAME, PLUGIN_WEB_ENTRYPOINT
from .context import ContextManager
from .file import FileUtils
from .renderer import Renderer
from .storage import Storage
from ..helpers.common import extract_multiline_value_from_yaml, get_app_version
from ..helpers.format import format_path, format_program
from ..models.base import AppDirs, EApp
from ..models.config import Config, Plugins, Privilege, Privileges, Rules
from ..models.context import Context
from ..models.plugin import BaseSettings, PluginContext, PluginManifest, PluginOutput
from ..models.users import Account, Extra, Users


class BasePlugin[T: BaseSettings](ABC):
    """Base class for all plugins."""

    manifest: ClassVar[PluginManifest]

    is_custom: ClassVar[bool] = False
    is_installable: ClassVar[bool] = False
    is_installed: ClassVar[bool] = False
    is_compatible: ClassVar[bool] = True
    alt_version: ClassVar[str | None] = None
    source: ClassVar[Path | None] = None

    is_rendered: ClassVar[bool] = False

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
        """
        Retrieve the settings class for the plugin.

        This method returns the class that defines the settings for the plugin. An instance of this class will be
        passed to the plugin during its initialization, which is set by the user.

        This method can be overridden in subclasses to provide custom settings classes. If not overridden, the default
        implementation returns the `BaseSettings` class.
        """
        return BaseSettings

    def get_custom_rendering_context(self) -> dict[str, Any]:
        """
        Retrieve the custom template rendering context.

        This method returns a dictionary that can be used to provide custom context data for template rendering.
        The returned dictionary can be accessed in the templates under the `plugin.custom` key.

        This method can be overridden in subclasses to provide custom context data. If not overridden, the default
        implementation returns an empty dictionary.
        """
        return {}

    def on_plugin_initialization(self) -> None:
        """
        Execute during the plugin initialization event.

        This method is invoked when the plugin is initialized. It can be used to perform actions like creating
        directories, generating secrets, etc.

        This method can be overridden in subclasses to provide custom initialization behavior. If not overridden, the
        default implementation does nothing.
        """
        ...

    def on_plugin_rendering(self) -> None:
        """
        Execute before the plugin rendering process.

        The rendering process is triggered when there are changes in the settings, the plugin itself, or the
        application. This method is intended to handle actions that cannot be performed with templates, such as
        updating database records.

        This method can be overridden in subclasses to provide custom behavior during the rendering process. If not
        overridden, the default implementation of this method does nothing.
        """
        ...

    @classmethod
    @final
    def mark_as_rendered(cls) -> None:
        cls.is_rendered = True

    @property
    @final
    def context(self) -> PluginContext:
        base_url = self.context_manager.config.network.base_url
        ip_addresses = self.context_manager.ip_addresses

        return PluginContext(
            manifest=self.manifest,
            backend_base_url=(
                f"http://{ip_addresses[self.manifest.name]}:{self.manifest.backend_port}/"
                if self.manifest.backend_port
                else None
            ),
            dirs=AppDirs(
                cache_dir=str(self.storage.cache_latest_dir / self.manifest.name),
                generated_dir=str(self.storage.generated_dir / self.manifest.name),
                managed_dir=str(self.storage.managed_dir / self.manifest.name),
                plugin_dir=os.path.join(".", self.storage.plugins_rel / self.manifest.name),
            ),
            ip_address=ip_addresses[self.manifest.name],
            oathkeeper_url_regex=f"{base_url}{PLUGIN_WEB_ENTRYPOINT}/<{self.manifest.web_path}>",
            web_base_url=f"{base_url}{PLUGIN_WEB_ENTRYPOINT}/{self.manifest.web_path}/",
            web_prefix=f"/{PLUGIN_WEB_ENTRYPOINT}/{self.manifest.web_path}",
            custom=self.get_custom_rendering_context(),
        )

    @property
    @final
    def output(self) -> PluginOutput:
        if self._output is None:
            if not self.is_rendered:
                self.console.print_error(f"Plugin {format_program(self.manifest.name)} has not been rendered.")
                raise Exit(code=1)

            plugin_dir = self.storage.installed_plugins_dir / self.manifest.name

            compose_content = self.file_utils.read_text(plugin_dir / "compose" / "compose.yaml", not_exist_ok=True)
            compose_services = extract_multiline_value_from_yaml(compose_content, "services")
            compose_secrets = extract_multiline_value_from_yaml(compose_content, "secrets")
            nginx_site = self.file_utils.read_text(plugin_dir / "nginx" / "site.conf", not_exist_ok=True)
            oathkeeper_rules = self.file_utils.read_text(
                plugin_dir / "oathkeeper" / "access_rules.yaml", not_exist_ok=True
            )
            web_dependencies = self.file_utils.read_text(
                plugin_dir / "web" / "dependencies.txt", not_exist_ok=True
            ).splitlines()

            self._output = PluginOutput(
                manifest=self.manifest,
                compose_services=compose_services,
                compose_secrets=compose_secrets,
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
        renderer: Renderer,
        storage: Storage,
    ):
        self.console = console
        self.context_manager = context_manager
        self.file_utils = file_utils
        self.renderer = renderer
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
                    plugin_cls.is_installable = True

                self._builtin_plugin_classes = plugin_classes

        return self._builtin_plugin_classes

    @property
    def custom_plugin_classes(self) -> list[type[BasePlugin]]:
        if self._custom_plugin_classes is None:
            plugin_classes = self.import_plugins(self.storage.custom_plugins_dir)

            for plugin_cls in plugin_classes:
                plugin_cls.is_custom = True
                plugin_cls.is_installable = True

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
                plugin_cls.is_installed = True

            self._installed_plugin_classes = plugin_classes

        return self._installed_plugin_classes

    @property
    def compatible_plugin_classes(self) -> list[type[BasePlugin]]:
        if self._compatible_plugin_classes is None:
            self._compatible_plugin_classes = [
                plugin_cls for plugin_cls in self.installed_plugin_classes if plugin_cls.is_compatible
            ]

        return self._compatible_plugin_classes

    @property
    def plugins(self) -> list[BasePlugin]:
        return self._plugins

    def add_plugin(self, plugin_cls: type[BasePlugin]) -> bool:
        """Add a plugin to the application."""
        if not plugin_cls.is_installable:
            self.console.print_warning(
                f"Plugin {format_program(plugin_cls.manifest.name)} is not installable. Skipping it."
            )
            return False

        dst = self.storage.installed_plugins_dir / plugin_cls.manifest.name

        if plugin_cls.is_custom:
            self.file_utils.copy(plugin_cls.source, dst)
        else:
            self.file_utils.copy_package_resources(f"{PACKAGE_NAME}.plugins", plugin_cls.manifest.name, dst)

        plugin_cls.is_installed = True
        return True

    def remove_plugin(self, plugin_cls: type[BasePlugin]) -> bool:
        """Remove a plugin from the application."""
        if not plugin_cls.is_installed:
            self.console.print_warning(
                f"Plugin {format_program(plugin_cls.manifest.name)} is not installed. Skipping it."
            )
            return False

        self.file_utils.remove(self.storage.installed_plugins_dir / plugin_cls.manifest.name)

        plugin_cls.is_installed = False
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
                plugin_version = plugin_cls.manifest.version

                try:
                    if get_app_version() not in SpecifierSet(plugin_cls.manifest.compatible_with):
                        self.console.print_warning(
                            f"Plugin {format_program(plugin_cls.manifest.name)} "
                            f"{f"version {plugin_version}" if plugin_version else "with an unknown version"} "
                            "is not compatible with the current version of the application. Skipping it."
                        )

                        plugin_cls.is_compatible = False
                except InvalidSpecifier:
                    self.console.print_warning(
                        f"Plugin {format_program(plugin_cls.manifest.name)} "
                        f"{f"version {plugin_version}" if plugin_version else "with an unknown version"} "
                        "has an invalid version specifier. Skipping it."
                    )

                    plugin_cls.is_compatible = False

                plugin_cls.source = plugin_dir
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
                extend_enum(EApp, plugin_cls.manifest.name.upper(), plugin_cls.manifest.name)

                settings_cls = plugin_cls.get_plugin_settings_cls()
                field_info = FieldInfo(annotation=settings_cls, default=settings_cls())
                Plugins.model_fields[plugin_cls.manifest.name] = field_info
            except Exception as e:
                self.console.print_warning(
                    f"Failed to load plugin {format_program(plugin_cls.manifest.name)} ({e}). Skipping it."
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
            plugin_settings = getattr(self.context_manager.config.plugins, plugin_cls.manifest.name, None)

            if plugin_settings is None:
                self.console.print_error(f"Settings for plugin {format_program(plugin_cls.manifest.name)} are missing.")
                raise Exit(code=1)

            plugin = plugin_cls(plugin_settings, self.console, self.context_manager, self.file_utils, self.storage)

            try:
                plugin.on_plugin_initialization()
            except Exit:
                raise
            except Exception as e:
                self.console.print_error(f"Failed to initialize plugin {format_program(plugin.manifest.name)} ({e}).")
                raise Exit(code=1)

            self.plugins.append(plugin)
            self.console.print_debug(f"Initialized plugin {format_program(plugin.manifest.name)}.")

    def render_plugins(self) -> None:
        """Render all plugins."""
        for plugin in self.plugins:
            try:
                plugin.on_plugin_rendering()
            except Exit:
                raise
            except Exception as e:
                self.console.print_error(f"Failed to render plugin {format_program(plugin.manifest.name)} ({e}).")
                raise Exit(code=1)

            self.renderer.render_plugin(plugin.manifest.name, plugin.context.model_dump())
            plugin.mark_as_rendered()

            self.context_manager.plugin_outputs.append(plugin.output)
            self.console.print_debug(f"Rendered plugin {format_program(plugin.manifest.name)}.")

    def update_rendered_plugin_files(self) -> None:
        for plugin in self.plugins:
            for web_dir in (self.storage.installed_plugins_dir / plugin.manifest.name / "web").iterdir():
                if web_dir.name == "lib":
                    dst_prefix = self.storage.bundled_dir / "web" / "src" / "lib" / "plugins"
                    self.file_utils.copy(web_dir, dst_prefix / plugin.manifest.name)
                elif web_dir.name == "routes":
                    dst_prefix = self.storage.bundled_dir / "web" / "src" / "routes" / "(apps)" / "app"
                    self.file_utils.copy(web_dir, dst_prefix / plugin.manifest.web_path)

        if self.context_manager.config.branding.cover:
            self.file_utils.copy(
                self.context_manager.config.branding.cover,
                self.storage.bundled_dir / "web" / "src" / "lib" / "assets" / "cover.jpg",
            )

        if self.context_manager.config.branding.logo:
            self.file_utils.copy(
                self.context_manager.config.branding.logo,
                self.storage.bundled_dir / "web" / "static" / "favicon.png",
            )
