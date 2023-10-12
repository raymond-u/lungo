from pathlib import Path
from typing import Annotated, Optional

from typer import Option

from ..app.state import console
from ..helpers.app import load_config, process_args


def main(
    config_dir: Annotated[
        Optional[Path], Option("--config-dir", "-c", help="Path to the configuration directory.", show_default=False)
    ] = None,
    quiet: Annotated[
        bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
    ] = False,
    verbosity: Annotated[
        int, Option("--verbose", "-v", count=True, help="Increase verbosity.", show_default=False)
    ] = 0,
) -> None:
    """
    Check if the configuration is valid.
    """
    process_args(config_dir, quiet, verbosity)
    load_config()

    console().print("Configuration is valid.")
