from typing import Annotated, Optional

from typer import Option

from .base import ConfigDirType, DevType, QuietType, VerbosityType
from ..app.state import app_manager, console, container
from ..core.constants import APP_NAME_CAPITALIZED
from ..models.base import EContainer


def main(
    container_tool: Annotated[
        Optional[EContainer], Option("--container-tool", help="Container management tool to use.", show_default=False)
    ] = None,
    config_dir: ConfigDirType = None,
    dev: DevType = False,
    quiet: QuietType = False,
    verbosity: VerbosityType = 0,
):
    """
    Stop the service.
    """
    app_manager().process_cli_options(config_dir, dev, quiet, verbosity)
    app_manager().load_core_config()

    container().set_preferred_tool(container_tool)

    with console().status("Stopping the service..."):
        container().down()

    console().print(f"{APP_NAME_CAPITALIZED} stopped.")
