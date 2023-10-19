from pathlib import Path
from typing import Annotated, Optional

from typer import Option

config_dir_type = Annotated[
    Optional[Path], Option("--config-dir", "-c", help="Path to the configuration directory.", show_default=False)
]
dev_type = Annotated[bool, Option("--dev", help="Use the development configuration.", show_default=False)]
force_init_type = Annotated[bool, Option("--force-init", help="Do a fresh initialization.", show_default=False)]
remove_lock_type = Annotated[bool, Option("--remove-lock", help="Remove the lock file.", show_default=False)]
quiet_type = Annotated[bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)]
verbosity_type = Annotated[int, Option("--verbose", "-v", count=True, help="Increase verbosity.", show_default=False)]
