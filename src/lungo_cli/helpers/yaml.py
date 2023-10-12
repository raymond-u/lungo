from os import PathLike
from typing import Type, TypeVar

from pydantic import BaseModel
from pydantic_yaml import parse_yaml_file_as
from typer import Exit

from .common import format_path
from ..app.state import console

T = TypeVar("T", bound=BaseModel)


def parse_yaml(path: str | PathLike[str], model: Type[T]) -> T:
    """Parse a YAML file as a Pydantic model."""
    try:
        return parse_yaml_file_as(model, path)
    except Exception as e:
        console().print_error(f"Failed to parse {format_path(path)} ({e}).")
        raise Exit(code=1)
