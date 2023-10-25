from typing import Annotated

from typer import Option

from .base import config_dir_type, dev_type, force_init_type, quiet_type, remove_lock_type, verbosity_type
from ..app.state import app_manager, console, container, context_manager
from ..core.constants import APP_NAME, APP_NAME_CAPITALIZED
from ..helpers.common import format_command, format_link


def main(
    build_only: Annotated[bool, Option("--build-only", help="Only build the container.", show_default=False)] = False,
    config_dir: config_dir_type = None,
    dev: dev_type = False,
    force_init: force_init_type = False,
    remove_lock: remove_lock_type = False,
    quiet: quiet_type = False,
    verbosity: verbosity_type = 0,
):
    """
    Start the service.
    """
    app_manager().process_args(config_dir, quiet, verbosity)
    app_manager().load_config()
    app_manager().process_args_delayed(dev, force_init, remove_lock)

    app_manager().ensure_application_data()

    if build_only:
        with console().status(
            "Building the container (it may take up to an hour depending on the internet connection)..."
        ):
            container().build()

        console().print("Build completed.")
    else:
        with console().status(
            "Starting the service (building may take up to an hour depending on the internet connection)..."
        ):
            container().up()

        console().print(
            f"{APP_NAME_CAPITALIZED} is now available at {format_link(context_manager().base_url)}."
            f"To stop it, run {format_command(APP_NAME, 'down')}."
        )
