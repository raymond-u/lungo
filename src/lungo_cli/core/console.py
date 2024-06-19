from contextlib import nullcontext
from enum import auto, Enum, IntEnum
from typing import Any, Callable

from rich import console
from rich.prompt import Confirm, Prompt
from rich.status import Status


class LogLevels(IntEnum):
    """Log levels for console output."""

    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class Console:
    """Console for text output."""

    def __init__(self):
        self.is_empty = True
        self.need_newline = False
        self.epilogue = []
        self.log_level = LogLevels.INFO
        self.stdout = console.Console()

    def set_log_level(self, verbosity: int):
        if verbosity <= -1:
            self.log_level = LogLevels.WARNING
        elif verbosity == 1:
            self.log_level = LogLevels.DEBUG
        elif verbosity >= 2:
            self.log_level = LogLevels.TRACE

    def ensure_newline(self):
        if self.need_newline:
            self.need_newline = False
            self.stdout.print()

        self.is_empty = False

    def request_newline(self):
        if not self.is_empty:
            self.need_newline = True

    def print(self, *args: Any, epilogue: bool = False, **kwargs: Any):
        kwargs["highlight"] = kwargs.get("highlight", False)

        if epilogue:
            self.epilogue.append((args, kwargs))
        else:
            self.ensure_newline()
            self.stdout.print(*args, **kwargs)

    def print_trace(self, *args: Any, **kwargs: Any):
        if self.log_level > LogLevels.TRACE:
            return

        self.print("[TRACE]", *args, **kwargs)

    def print_debug(self, *args: Any, **kwargs: Any):
        if self.log_level > LogLevels.DEBUG:
            return

        self.print("[DEBUG]", *args, **kwargs)

    def print_info(self, *args: Any, **kwargs: Any):
        if self.log_level > LogLevels.INFO:
            return

        self.print("[INFO]", *args, **kwargs)

    def print_warning(self, *args: Any, **kwargs: Any):
        if self.log_level > LogLevels.WARNING:
            return

        self.print("[bold yellow][WARNING][/bold yellow]", *args, **kwargs)

    def print_error(self, *args: Any, **kwargs: Any):
        if self.log_level > LogLevels.ERROR:
            return

        self.print("[bold red][ERROR][/bold red]", *args, **kwargs)

    def show_epilogue(self):
        self.request_newline()
        self.ensure_newline()

        for args, kwargs in self.epilogue:
            self.stdout.print(*args, **kwargs)

        self.epilogue.clear()

    def ask_for_boolean(self, prompt: str, default: bool = True, **kwargs: Any) -> bool:
        self.ensure_newline()

        kwargs["prompt"] = f"[bold]{prompt}[/bold] " + ("[Y/n]" if default else "[y/N]")
        kwargs["default"] = default
        kwargs["show_default"] = False
        kwargs["show_choices"] = False

        return Confirm.ask(**kwargs)

    def ask_for_integer(
        self, prompt: str, default: int | None = None, guard: Callable[[int], bool] = lambda x: True, **kwargs: Any
    ) -> int:
        self.ensure_newline()

        kwargs["prompt"] = f"[bold]{prompt}[/bold]"
        kwargs["default"] = default or None
        kwargs["show_default"] = default is not None

        while not (answer := Prompt.ask(**kwargs)).isdigit() or not guard(int(answer)):
            self.print_warning("Invalid input. Please try again.")

        return int(answer)

    def ask_for_string(
        self, prompt: str, default: str | None = None, guard: Callable[[str], bool] = lambda x: bool(x), **kwargs: Any
    ) -> str:
        self.ensure_newline()

        kwargs["prompt"] = f"[bold]{prompt}[/bold]"
        kwargs["default"] = default or None
        kwargs["show_default"] = bool(default)

        while not guard(answer := Prompt.ask(**kwargs)):
            self.print_warning("Invalid input. Please try again.")

        return answer

    def ask_for_password(self, prompt: str, **kwargs: Any) -> str:
        self.ensure_newline()

        kwargs["prompt"] = f"[bold]{prompt}[/bold]"
        kwargs["password"] = True
        kwargs["default"] = None
        kwargs["show_default"] = False

        while True:
            answer = Prompt.ask(**kwargs)
            kwargs["prompt"] = "[bold]Please enter the password again[/bold]"

            if Prompt.ask(**kwargs) == answer:
                break
            else:
                self.print_warning("Passwords do not match. Please try again.")

        return answer

    def ask_for_enum[T: Enum](self, prompt: str, enum: type[T], default: T | None = None, **kwargs: Any) -> T:
        self.ensure_newline()

        kwargs["prompt"] = f"[bold]{prompt}[/bold]"
        kwargs["choices"] = [e.value for e in enum]
        kwargs["default"] = default.value if default else None

        while not (answer := Prompt.ask(**kwargs)):
            self.print_warning("Invalid input. Please try again.")

        return enum(answer)

    def ask_for_list(self, prompt: str, default: list[str] | None = None, **kwargs: Any) -> list[str]:
        self.ensure_newline()

        kwargs["prompt"] = f"[bold]{prompt}[/bold] (leave blank to finish)"
        kwargs["default"] = default or None

        if not (answer := Prompt.ask(**kwargs)):
            return []

        answers = [answer]

        while answer := input():
            answers.append(answer)

        return answers

    def status(self, status: str, **kwargs: Any) -> Status | nullcontext:
        if self.log_level.value > LogLevels.INFO.value:
            return nullcontext()

        kwargs["status"] = status
        return self.stdout.status(**kwargs)
