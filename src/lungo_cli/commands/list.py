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

    plugin_classes = plugin_manager().installed_plugin_classes

    for installable_plugin_cls in plugin_manager().installable_plugin_classes:
        if plugin_cls := next(
            (x for x in plugin_classes if x.manifest.name == installable_plugin_cls.manifest.name), None
        ):
            plugin_cls.is_installable = True
            plugin_cls.alt_version = installable_plugin_cls.manifest.version
        else:
            installable_plugin_cls.alt_version = installable_plugin_cls.manifest.version
            plugin_classes.append(installable_plugin_cls)

    if args:
        for arg in args:
            if plugin_cls := next((x for x in plugin_classes if x.manifest.name == arg), None):
                console().print(
                    f"Name: {plugin_cls.manifest.name}"
                    f"{f' ({plugin_cls.manifest.descriptive_name})' if plugin_cls.manifest.descriptive_name else ''}"
                )
                console().print(
                    f"Version: {plugin_cls.manifest.version if plugin_cls.is_installed else '-'} -> {plugin_cls.alt_version}"
                    if plugin_cls.is_installable
                    else ""
                )
                console().print(f"Category: {'custom' if plugin_cls.is_custom else 'built-in'} plugin")
                console().print(f"Description: {plugin_cls.manifest.description or 'No description.'}")
            else:
                console().print(f"Plugin {format_input(arg)} not found. Skipping it.")

            console().request_newline()
    else:
        if len(plugin_classes) == 0:
            console().print("No plugins found.")
            return

        plugin_classes.sort(key=lambda x: x.manifest.name)
        plugin_classes.sort(key=lambda x: not x.is_installed)

        table = Table()
        table.add_column("Name")
        table.add_column("Current")
        table.add_column("Available")

        for plugin_cls in plugin_classes:
            table.add_row(
                plugin_cls.manifest.name,
                plugin_cls.manifest.version if plugin_cls.is_installed else "-",
                plugin_cls.alt_version if plugin_cls.is_installable else "-",
            )

        console().print(table)
