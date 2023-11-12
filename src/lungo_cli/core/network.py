import time
from typing import Any

import requests
from typer import Exit

from .console import Console
from ..helpers.format import format_path


class HttpApiClient:
    """HTTP API client for sending and receiving JSON data."""

    def __init__(self, console: Console):
        self.console = console

    def ensure_reachable(self, url: str) -> None:
        while True:
            try:
                self.console.print_debug(f"Checking if {format_path(url)} is reachable...")
                requests.get(url, headers={"Accept": "application/json"}).raise_for_status()
                break
            except Exception as e:
                self.console.print_debug(f"Waiting for {format_path(url)} to be reachable ({e})...")
                time.sleep(2)

                continue

    def get(self, url: str) -> Any:
        try:
            self.console.print_debug(f"Sending GET request to {format_path(url)}...")
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()

            return response.json()
        except Exception as e:
            self.console.print_error(f"Failed to send GET request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def post(self, url: str, data: Any) -> Any:
        try:
            self.console.print_debug(f"Sending POST request to {format_path(url)}...")
            response = requests.post(url, json=data, headers={"Accept": "application/json"})
            response.raise_for_status()

            return response.json()
        except Exception as e:
            self.console.print_error(f"Failed to send POST request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def delete(self, url: str) -> None:
        try:
            self.console.print_debug(f"Sending DELETE request to {format_path(url)}...")
            response = requests.delete(url, headers={"Accept": "application/json"})
            response.raise_for_status()
        except Exception as e:
            self.console.print_error(f"Failed to send DELETE request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def patch(self, url: str, data: Any) -> None:
        try:
            self.console.print_debug(f"Sending PATCH request to {format_path(url)}...")
            response = requests.patch(url, json=data, headers={"Accept": "application/json"})
            response.raise_for_status()
        except Exception as e:
            self.console.print_error(f"Failed to send PATCH request to {format_path(url)} ({e}).")
            raise Exit(code=1)
