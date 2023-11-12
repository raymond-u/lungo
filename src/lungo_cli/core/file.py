import hashlib
import shutil
from os import PathLike
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError
from pydantic_yaml import parse_yaml_file_as
from typer import Exit

from .console import Console
from ..helpers.format import format_path

T = TypeVar("T", bound=BaseModel)


class FileUtils:
    """File utilities."""

    def __init__(self, console: Console):
        self.console = console

    def create(self, path: str | PathLike[str]) -> None:
        path = Path(path)

        try:
            self.create_dir(path.parent)
            path.touch()
        except Exception as e:
            self.console.print_error(f"Failed to create {format_path(path.name)} ({e}).")
            raise Exit(code=1)

    def create_dir(self, path: str | PathLike[str]) -> None:
        path = Path(path)

        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.console.print_error(f"Failed to create {format_path(path.name)} ({e}).")
            raise Exit(code=1)

    def copy(self, src: str | PathLike[str], dst: str | PathLike[str]) -> None:
        src = Path(src)
        dst = Path(dst)

        try:
            self.create_dir(dst.parent)
            self.remove(dst)

            if src.is_dir():
                shutil.copytree(src, dst)
            elif src.is_file():
                shutil.copy(src, dst)
            else:
                self.console.print_error(f"{format_path(src.name)} is not a file or directory.")
                raise Exit(code=1)
        except Exception as e:
            self.console.print_error(f"Failed to copy {format_path(src.name)} to {format_path(dst.name)} ({e}).")
            raise Exit(code=1)

    def copy_to(self, src: str | PathLike[str], dst_dir: str | PathLike[str]) -> None:
        src = Path(src)
        dst_dir = Path(dst_dir)

        self.copy(src, dst_dir / src.name)

    def remove(self, path: str | PathLike[str]) -> None:
        path = Path(path)

        try:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.is_file():
                path.unlink()
        except Exception as e:
            self.console.print_error(f"Failed to remove {format_path(path.name)} ({e}).")
            raise Exit(code=1)

    def read_text(self, path: str | PathLike[str]) -> str:
        path = Path(path)

        try:
            return path.read_text()
        except Exception as e:
            self.console.print_error(f"Failed to read {format_path(path.name)} ({e}).")
            raise Exit(code=1)

    def write_bytes(self, path: str | PathLike[str], data: bytes, secret: bool = False) -> None:
        path = Path(path)

        try:
            self.create_dir(path.parent)
            path.write_bytes(data)

            if secret:
                self.change_mode(path, 0o600)
        except Exception as e:
            self.console.print_error(f"Failed to write {format_path(path.name)} ({e}).")
            raise Exit(code=1)

    def write_text(self, path: str | PathLike[str], text: str, secret: bool = False) -> None:
        path = Path(path)

        try:
            self.create_dir(path.parent)
            path.write_text(text)

            if secret:
                self.change_mode(path, 0o600)
        except Exception as e:
            self.console.print_error(f"Failed to write {format_path(path.name)} ({e}).")
            raise Exit(code=1)

    def change_mode(self, path: str | PathLike[str], mode: int) -> None:
        path = Path(path)

        try:
            path.chmod(mode)
        except Exception as e:
            self.console.print_error(f"Failed to change mode of {format_path(path.name)} ({e}).")
            raise Exit(code=1)

    def hash_sha256(self, path: str | PathLike[str]) -> str:
        path = Path(path)

        try:
            with open(path, "rb") as f:
                return hashlib.file_digest(f, "sha256").hexdigest()
        except Exception as e:
            self.console.print_error(f"Failed to hash {format_path(path.name)} ({e}).")
            raise Exit(code=1)

    def parse_yaml(self, path: str | PathLike[str], model: Type[T]) -> T:
        """Parse a YAML file as a Pydantic model."""
        try:
            return parse_yaml_file_as(model, path)
        except ValidationError as e:
            error_msg = f"Failed to parse {format_path(path)}."

            for error in e.errors():
                error_msg += "\n  * "

                if error["loc"]:
                    for loc in error["loc"]:
                        if type(loc) is int:
                            error_msg += f"[{loc}]"
                        else:
                            error_msg += f".{loc}"
                else:
                    error_msg += "root"

                error_msg += f": {error['msg']}"

            self.console.print_error(error_msg)
            raise Exit(code=1)
        except Exception as e:
            self.console.print_error(f"Failed to parse {format_path(path)} ({e}).")
            raise Exit(code=1)
