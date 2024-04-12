from os import PathLike
from typing import Any

from jinja2 import Environment, FileSystemLoader
from typer import Exit

from .console import Console
from .context import ContextManager
from .file import FileUtils
from .plugin import BasePlugin
from .storage import Storage
from ..helpers.format import format_path, format_program


class Renderer:
    """Render Jinja templates."""

    def __init__(self, console: Console, context_manager: ContextManager, file_utils: FileUtils, storage: Storage):
        self.console = console
        self.context_manager = context_manager
        self.file_utils = file_utils
        self.storage = storage

        self._env = None

    @property
    def env(self) -> Environment:
        if not self._env:
            self._env = Environment(
                autoescape=False,
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

    def render_main(self) -> None:
        self.console.print_info("Rendering templates...")

        for file in self.storage.bundled_dir.rglob("*.jinja"):
            relative_path = file.relative_to(self.storage.bundled_dir)

            if relative_path.parts[0] not in [str(self.storage.excluded_rel), str(self.storage.plugins_rel)]:
                self.render(relative_path, file.with_suffix(""), **self.context_manager.context.model_dump())

    def render_plugin(self, plugin: BasePlugin) -> None:
        self.console.print_info(f"Rendering templates for {format_program(plugin.config.name)}...")

        for file in self.storage.installed_plugins_dir.joinpath(plugin.config.name).rglob("*.jinja"):
            relative_path = file.relative_to(self.storage.bundled_dir)
            self.render(
                relative_path,
                file.with_suffix(""),
                **self.context_manager.context.model_dump(),
                **plugin.get_render_context(),
            )

        plugin.mark_as_rendered()
