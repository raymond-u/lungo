from typing import Annotated, Optional

from typer import Option

from .base import config_dir_type, dev_type, quiet_type, verbosity_type
from ..app.state import app_manager, console, container
from ..core.constants import APP_NAME_CAPITALIZED
from ..models.base import EContainer


def main(
    container_tool: Annotated[
        Optional[EContainer], Option("--container-tool", help="Container management tool to use.", show_default=False)
    ] = None,
    config_dir: config_dir_type = None,
    dev: dev_type = False,
    quiet: quiet_type = False,
    verbosity: verbosity_type = 0,
):
    """
    Stop the service.
    """
    app_manager().process_args(config_dir, quiet, verbosity)
    app_manager().load_config()
    app_manager().process_args_deferred(dev)

    container().set_preferred_tool(container_tool)

    with console().status("Stopping the service..."):
        container().down()

    console().print(f"{APP_NAME_CAPITALIZED} stopped.")
