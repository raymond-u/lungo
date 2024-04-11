from .base import ConfigDirType, DevType, QuietType, VerbosityType
from ..app.state import app_manager, console


def main(
    config_dir: ConfigDirType = None,
    dev: DevType = False,
    quiet: QuietType = False,
    verbosity: VerbosityType = 0,
) -> None:
    """
    Check if the configuration is valid.
    """
    app_manager().process_cli_options(config_dir, dev, quiet, verbosity)
    app_manager().load_full_config()

    console().print("Configuration is valid.")
