import time
from typing import Any

import requests
from typer import Exit

from .console import Console
from ..helpers.common import format_path


class HttpApiClient:
    def __init__(self, console: Console):
        self.console = console

    def ensure_reachable(self, url: str) -> None:
        while True:
            try:
                requests.get(url, headers={"Accept": "application/json"}).raise_for_status()
                break
            except Exception as e:
                self.console.print_debug(f"Waiting for {format_path(url)} to be reachable ({e})...")
                time.sleep(2)

                continue

    def get(self, url: str) -> Any:
        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()

            return response.json()
        except Exception as e:
            self.console.print_error(f"Failed to send GET request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def post(self, url: str, data: Any) -> Any:
        try:
            response = requests.post(url, json=data, headers={"Accept": "application/json"})
            response.raise_for_status()

            return response.json()
        except Exception as e:
            self.console.print_error(f"Failed to send POST request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def delete(self, url: str) -> None:
        try:
            response = requests.delete(url, headers={"Accept": "application/json"})
            response.raise_for_status()
        except Exception as e:
            self.console.print_error(f"Failed to send DELETE request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def patch(self, url: str, data: Any) -> None:
        try:
            response = requests.patch(url, json=data, headers={"Accept": "application/json"})
            response.raise_for_status()
        except Exception as e:
            self.console.print_error(f"Failed to send PATCH request to {format_path(url)} ({e}).")
            raise Exit(code=1)
