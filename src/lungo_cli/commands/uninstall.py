from typing import Annotated

from typer import Argument

from .base import config_dir_type, dev_type, quiet_type, verbosity_type
from ..app.state import app_manager, console, plugin_manager
from ..helpers.format import format_input


def main(
    args: Annotated[
        list[str],
        Argument(
            help="Names of the plugins to remove.",
            show_default=False,
        ),
    ],
    config_dir: config_dir_type = None,
    dev: dev_type = False,
    quiet: quiet_type = False,
    verbosity: verbosity_type = 0,
) -> None:
    """
    Uninstall plugins.
    """
    app_manager().process_cli_options(config_dir, dev, quiet, verbosity)
    app_manager().load_core_config()

    count = 0

    for arg in args:
        plugin_cls = next((x for x in plugin_manager().installed_plugin_classes if x.config.name == arg), None)

        if plugin_cls is None:
            console().print_warning(f"Plugin {format_input(arg)} not found or not installed. Skipping.")
            continue

        if plugin_manager().remove_plugin(plugin_cls):
            count += 1

    if count == 1:
        console().print("1 plugin removed successfully.")
    elif count > 1:
        console().print(f"{count} plugins removed successfully.")
