from pathlib import Path
from typing import Annotated, Optional

from typer import Option

from ..app.state import console, container
from ..core.constants import APP_NAME_CAPITALIZED
from ..helpers.app import load_config, process_args, process_args_delayed


def main(
    config_dir: Annotated[
        Optional[Path], Option("--config-dir", "-c", help="Path to the configuration directory.", show_default=False)
    ] = None,
    dev: Annotated[bool, Option("--dev", help="Use the development configuration.", show_default=False)] = False,
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
    verbosity: Annotated[
        int, Option("--verbose", "-v", count=True, help="Increase verbosity.", show_default=False)
    ] = 0,
):
    """
    Stop the service.
    """
    process_args(config_dir, quiet, verbosity)
    load_config()
    process_args_delayed(dev)

    with console().status("Stopping the service..."):
        container().down()

    console().print(f"{APP_NAME_CAPITALIZED} stopped.")
