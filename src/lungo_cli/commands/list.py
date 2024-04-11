from typing import Annotated, Optional

from rich.table import Table
from typer import Argument

from .base import ConfigDirType, DevType, QuietType, VerbosityType
from ..app.state import app_manager, console, plugin_manager
from ..helpers.format import format_input


def main(
    args: Annotated[
        Optional[list[str]],
        Argument(
            help="Names of the plugins to list.",
            show_default=False,
        ),
    ] = None,
    config_dir: ConfigDirType = None,
    dev: DevType = False,
    quiet: QuietType = False,
    verbosity: VerbosityType = 0,
) -> None:
    """
    List all plugins.
    """
    app_manager().process_cli_options(config_dir, dev, quiet, verbosity)
    app_manager().load_core_config()

    plugin_classes = plugin_manager().compatible_plugin_classes

    for installable_plugin_cls in plugin_manager().installable_plugin_classes:
        if plugin_cls := next((x for x in plugin_classes if x.config.name == installable_plugin_cls.config.name), None):
            plugin_cls.installable = True
            plugin_cls.alt_version = installable_plugin_cls.config.version
        else:
            installable_plugin_cls.alt_version = installable_plugin_cls.config.version
            plugin_classes.append(installable_plugin_cls)

    if args:
        for arg in args:
            if plugin_cls := next((x for x in plugin_classes if x.config.name == arg), None):
                console().print(
                    f"Name: {plugin_cls.config.name}"
                    f"{f' ({plugin_cls.config.descriptive_name})' if plugin_cls.config.descriptive_name else ''}"
                )
                console().print(
                    f"Version: {(plugin_cls.installed and plugin_cls.config.version) or '-'}"
                    f" -> {(plugin_cls.installable and plugin_cls.alt_version) or '-'}"
                    if plugin_cls.installable
                    else ""
                )
                console().print(
                    f"Status: {'installable' if plugin_cls.installable else 'not installable'}, "
                    f"{'installed' if plugin_cls.installed else 'not installed'} "
                    f"({'custom' if plugin_cls.custom else 'built-in'} plugin)."
                )
                console().print(f"Description: {plugin_cls.config.description or 'No description.'}")
            else:
                console().print(f"Plugin {format_input(arg)} not found. Skipping it.")

            console().request_newline()
    else:
        if len(plugin_classes) == 0:
            console().print("No plugins found.")
            return

        plugin_classes.sort(key=lambda x: x.config.name)
        plugin_classes.sort(key=lambda x: not x.installed)

        table = Table()
        table.add_column("Name")
        table.add_column("Current")
        table.add_column("Available")
        table.add_column("Installable")
        table.add_column("Installed")

        for plugin_cls in plugin_classes:
            table.add_row(
                plugin_cls.config.name,
                (plugin_cls.installed and plugin_cls.config.version) or "-",
                (plugin_cls.installable and plugin_cls.alt_version) or "-",
                "Yes" if plugin_cls.installable else "No",
                "Yes" if plugin_cls.installed else "No",
            )

        console().print(table)
