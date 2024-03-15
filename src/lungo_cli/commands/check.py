from .base import config_dir_type, dev_type, quiet_type, verbosity_type
from ..app.state import app_manager, console


def main(
    config_dir: config_dir_type = None,
    dev: dev_type = False,
    quiet: quiet_type = False,
    verbosity: verbosity_type = 0,
) -> None:
    """
    Check if the configuration is valid.
    """
    app_manager().process_args(config_dir, dev, quiet, verbosity)
    app_manager().load_config_and_plugins()

    console().print("Configuration is valid.")
