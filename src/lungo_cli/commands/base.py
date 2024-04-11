from pathlib import Path
from typing import Annotated, Final, Optional

from typer import Option

ConfigDirType: Final[type[Optional[Path]]] = Annotated[
    Optional[Path], Option("--config-dir", "-c", help="Path to the configuration directory.", show_default=False)
]
DevType: Final[type[bool]] = Annotated[
    bool, Option("--dev", help="Use the development configuration.", show_default=False)
]
ForceInitType: Final[type[bool]] = Annotated[
    bool, Option("--force-init", help="Do a fresh initialization.", show_default=False)
]
QuietType: Final[type[bool]] = Annotated[
    bool, Option("--quiet", "-q", help="Suppress all output except for errors.", show_default=False)
]
VerbosityType: Final[type[int]] = Annotated[
    int, Option("--verbose", "-v", count=True, help="Increase verbosity.", show_default=False)
]
