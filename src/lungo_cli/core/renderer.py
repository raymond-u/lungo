from os import PathLike
from typing import Any

from jinja2 import Environment, FileSystemLoader
from typer import Exit

from .console import Console
from .file import FileUtils
from .storage import Storage
from ..helpers.format import format_path
from ..models.context import Context


class Renderer:
    """Render Jinja templates."""

    def __init__(self, console: Console, file_utils: FileUtils, storage: Storage):
        self.console = console
        self.file_utils = file_utils
        self.storage = storage
        self._env = None

    @property
    def env(self) -> Environment:
        if not self._env:
            self._env = Environment(
                autoescape=True,
                lstrip_blocks=True,
                trim_blocks=True,
                loader=FileSystemLoader(self.storage.bundled_dir),
            )

        return self._env

    def render(self, src: str | PathLike[str], dst: str | PathLike[str], **kwargs: Any) -> None:
        try:
            self.console.print_debug(f"Rendering {format_path(src)}...")
            self.file_utils.write_text(dst, self.env.get_template(str(src)).render(**kwargs))
        except Exception as e:
            self.console.print_error(f"Failed to render {format_path(src)} ({e}).")
            raise Exit(code=1)

    def render_all(self, context: Context) -> None:
        self.console.print_info("Rendering templates...")

        for file in self.storage.bundled_dir.rglob("*.jinja"):
            relative_path = file.relative_to(self.storage.bundled_dir)

            if str(self.storage.excluded_rel) not in relative_path.parts:
                self.render(relative_path, file.with_suffix(""), **context.model_dump())
