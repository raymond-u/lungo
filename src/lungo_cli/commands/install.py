from typing import Annotated

from typer import Argument

from .base import ConfigDirType, DevType, QuietType, VerbosityType
from ..app.state import app_manager, console, plugin_manager
from ..helpers.format import format_input


def main(
    args: Annotated[
        list[str],
        Argument(
            help="Names of the plugins to add.",
            show_default=False,
        ),
    ],
    config_dir: ConfigDirType = None,
    dev: DevType = False,
    quiet: QuietType = False,
    verbosity: VerbosityType = 0,
) -> None:
    """
    Install or upgrade plugins.
    """
    app_manager().process_cli_options(config_dir, dev, quiet, verbosity)
    app_manager().load_core_config()

    count = 0

    for arg in args:
        plugin_cls = next((x for x in plugin_manager().installable_plugin_classes if x.manifest.name == arg), None)

        if plugin_cls is None:
            console().print_warning(f"Plugin {format_input(arg)} not found or not installable. Skipping it.")
            continue

        if plugin_manager().add_plugin(plugin_cls):
            count += 1

    if count == 1:
        console().print("1 plugin added successfully.")
    elif count > 1:
        console().print(f"{count} plugins added successfully.")
