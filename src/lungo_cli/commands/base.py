from pathlib import Path
from typing import Annotated, Final, Optional

from typer import Option

ConfigDirType: Final = Annotated[
    Optional[Path], Option("--config-dir", "-c", help="Path to the configuration directory.", show_default=False)
]
DevType: Final = Annotated[bool, Option("--dev", help="Use the development configuration.", show_default=False)]
ForceInitType: Final = Annotated[bool, Option("--force-init", help="Do a fresh initialization.", show_default=False)]
QuietType: Final = Annotated[
    bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
]
VerbosityType: Final = Annotated[
    int, Option("--verbose", "-v", count=True, help="Increase verbosity.", show_default=False)
]
