from typing import Annotated, Optional

from typer import Option

from .base import ConfigDirType, DevType, ForceInitType, QuietType, VerbosityType
from ..app.state import app_manager, console, container, context_manager, file_utils, storage
from ..core.constants import APP_NAME, APP_NAME_CAPITALIZED
from ..helpers.format import format_command, format_link
from ..models.base import EContainer


def main(
    build_only: Annotated[bool, Option("--build-only", help="Only build the containers.", show_default=False)] = False,
    container_tool: Annotated[
        Optional[EContainer], Option("--container-tool", help="Container management tool to use.", show_default=False)
    ] = None,
    render_only: Annotated[
        bool, Option("--render-only", help="Only render the templates.", show_default=False)
    ] = False,
    force_init: ForceInitType = False,
    remove_lock: Annotated[bool, Option("--remove-lock", help="Remove the lock file.", show_default=False)] = False,
    config_dir: ConfigDirType = None,
    dev: DevType = False,
    quiet: QuietType = False,
    verbosity: VerbosityType = 0,
):
    """
    Start the service.
    """
    app_manager().process_cli_options(config_dir, dev, quiet, verbosity, force_init)
    app_manager().load_full_config()

    if remove_lock:
        file_utils().remove(storage().lock_file)

    app_manager().initialize()

    if render_only:
        return

    container().set_preferred_tool(container_tool)

    if build_only:
        with console().status(
            "Building containers (could take a few minutes, depending on the internet connection)..."
        ):
            container().build()

        console().print("Build completed.")
    else:
        app_manager().ensure_port_availability()

        with console().status(
            "Starting the service (could take a few minutes, depending on the internet connection)..."
        ):
            container().up()

        console().print(
            f"{APP_NAME_CAPITALIZED} is now available at {format_link(context_manager().config.network.base_url)}. "
            f"To stop it, run {format_command(APP_NAME, 'down', '--dev' if context_manager().dev else '')}."
        )
