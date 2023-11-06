---
hide:
    - navigation
---

# Installation

## With pipx

The recommended way to install Lungo is using [pipx](https://pypa.github.io/pipx/):

```bash linenums="1" title="Terminal"
pipx install lungo-cli
```

## With pip

To install Lungo using pip, run:

```bash linenums="1" title="Terminal"
pip install lungo-cli
```

## Installing from source

To install from source, run:

```bash linenums="1" title="Terminal"
git clone --recurse-submodules https://github.com/raymond-u/lungo
cd lungo
pip install .
```

## Notes

Lungo is built upon [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). Before
proceeding, please ensure that both Docker and Docker Compose are installed on your machine.

Alternatively, you can use [Podman](https://podman.io/)
and [Podman Compose](https://github.com/containers/podman-compose).

For instructions on installing these tools, please refer to their respective documentation.
