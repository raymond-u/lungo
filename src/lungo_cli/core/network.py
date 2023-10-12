import time
from typing import Any

import requests
from requests import ConnectTimeout
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
            except ConnectTimeout:
                time.sleep(1)
                continue
            except Exception as e:
                self.console.print_error(f"Failed to connect to {format_path(url)} ({e}).")
                raise Exit(code=1)

    def get(self, url: str) -> Any:
        try:
            response = requests.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()

            return response.json()
        except Exception as e:
            self.console.print_error(f"Failed to send GET request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def delete(self, url: str) -> Any:
        try:
            response = requests.delete(url, headers={"Accept": "application/json"})
            response.raise_for_status()

            return response.json()
        except Exception as e:
            self.console.print_error(f"Failed to send DELETE request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def post(self, url: str, data: Any) -> Any:
        try:
            response = requests.post(url, json=data, headers={"Accept": "application/json"})
            response.raise_for_status()

            return response.json()
        except Exception as e:
            self.console.print_error(f"Failed to send POST request to {format_path(url)} ({e}).")
            raise Exit(code=1)

    def patch(self, url: str, data: Any) -> Any:
        try:
            response = requests.patch(url, json=data, headers={"Accept": "application/json"})
            response.raise_for_status()

            return response.json()
        except Exception as e:
            self.console.print_error(f"Failed to send PATCH request to {format_path(url)} ({e}).")
            raise Exit(code=1)
