from .base import config_dir_type, dev_type, quiet_type, verbosity_type
from ..app.state import app_manager, console, container
from ..core.constants import APP_NAME_CAPITALIZED


def main(
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
    app_manager().process_args_delayed(dev)

    with console().status("Stopping the service..."):
        container().down()

    console().print(f"{APP_NAME_CAPITALIZED} stopped.")
