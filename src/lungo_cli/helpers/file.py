import hashlib
import shutil
from os import PathLike
from pathlib import Path

from typer import Exit

from .common import format_path
from ..app.state import console


def create(path: str | PathLike[str]) -> None:
    path = Path(path)

    try:
        create_dir(path.parent)
        path.touch()
    except Exception as e:
        console().print_error(f"Failed to create {format_path(path.name)} ({e}).")
        raise Exit(code=1)


def create_dir(path: str | PathLike[str]) -> None:
    path = Path(path)

    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console().print_error(f"Failed to create {format_path(path.name)} ({e}).")
        raise Exit(code=1)


def copy(src: str | PathLike[str], dst: str | PathLike[str]) -> None:
    src = Path(src)
    dst = Path(dst)

    try:
        create_dir(dst.parent)
        remove(dst)

        if src.is_dir():
            shutil.copytree(src, dst)
        elif src.is_file():
            shutil.copy(src, dst)
        else:
            console().print_error(f"{format_path(src.name)} is not a file or directory.")
            raise Exit(code=1)
    except Exit:
        raise
    except Exception as e:
        console().print_error(f"Failed to copy {format_path(src.name)} to {format_path(dst.name)} ({e}).")
        raise Exit(code=1)


def copy_to(src: str | PathLike[str], dst_dir: str | PathLike[str]) -> None:
    src = Path(src)
    dst_dir = Path(dst_dir)

    copy(src, dst_dir / src.name)


def remove(path: str | PathLike[str]) -> None:
    path = Path(path)

    try:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()
    except Exception as e:
        console().print_error(f"Failed to remove {format_path(path.name)} ({e}).")
        raise Exit(code=1)


def read_text(path: str | PathLike[str]) -> str:
    path = Path(path)

    try:
        return path.read_text()
    except Exception as e:
        console().print_error(f"Failed to read {format_path(path.name)} ({e}).")
        raise Exit(code=1)


def write_bytes(path: str | PathLike[str], data: bytes) -> None:
    path = Path(path)

    try:
        path.write_bytes(data)
    except Exception as e:
        console().print_error(f"Failed to write {format_path(path.name)} ({e}).")
        raise Exit(code=1)


def write_text(path: str | PathLike[str], text: str) -> None:
    path = Path(path)

    try:
        path.write_text(text)
    except Exception as e:
        console().print_error(f"Failed to write {format_path(path.name)} ({e}).")
        raise Exit(code=1)


def hash_sha256(path: str | PathLike[str]) -> str:
    path = Path(path)

    try:
        with open(path, "rb") as f:
            return hashlib.file_digest(f, "sha256").hexdigest()
    except Exception as e:
        console().print_error(f"Failed to hash {format_path(path.name)} ({e}).")
        raise Exit(code=1)
