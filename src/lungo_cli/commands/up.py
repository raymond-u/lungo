from pathlib import Path
from typing import Annotated, Optional

from typer import Option

from ..app.state import console, container
from ..core.constants import APP_NAME, APP_NAME_CAPITALIZED
from ..helpers.app import ensure_application_data, load_config, process_args, process_args_delayed
from ..helpers.common import format_command, format_path


def main(
    build_only: Annotated[bool, Option("--build-only", help="Only build the container.", show_default=False)] = False,
    config_dir: Annotated[
        Optional[Path], Option("--config-dir", "-c", help="Path to the configuration directory.", show_default=False)
    ] = None,
    dev: Annotated[bool, Option("--dev", help="Use the development configuration.", show_default=False)] = False,
    force_init: Annotated[bool, Option("--force-init", help="Do a fresh initialization.", show_default=False)] = False,
    remove_lock: Annotated[bool, Option("--remove-lock", help="Remove the lock file.", show_default=False)] = False,
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
    verbosity: Annotated[
        int, Option("--verbose", "-v", count=True, help="Increase verbosity.", show_default=False)
    ] = 0,
):
    """
    Start the service.
    """
    process_args(config_dir, quiet, verbosity)
    config, users = load_config()
    process_args_delayed(dev, force_init, remove_lock)

    ensure_application_data(config, users)

    if build_only:
        with console().status(
            "Building the container (if this is the first time, it may take up to an hour "
            "depending on your internet connection)..."
        ):
            container().build()

        console().print("Build completed.")
    else:
        with console().status(
            "Starting the service (if this is the first time, it may take up to an hour "
            "depending on your internet connection)..."
        ):
            container().up()

        console().print(
            f"{APP_NAME_CAPITALIZED} is now available at {format_path(f'https://{config.network.hostname}/')}. "
            f"To stop it, run {format_command(APP_NAME, 'down')}."
        )
