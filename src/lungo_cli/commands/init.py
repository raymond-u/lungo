from pathlib import Path
from typing import Annotated, Optional

from typer import Option

from ..app.state import console, container
from ..helpers.app import ensure_application_data, load_config, process_args, process_args_delayed


def main(
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
    Perform the initial setup of the application.
    """
    process_args(config_dir, quiet, verbosity)
    config, users = load_config()
    process_args_delayed(dev, force_init, remove_lock)

    ensure_application_data(config, users)

    with console().status("Building the container..."):
        container().build()

    console().print("Initialization completed.")
