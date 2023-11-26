---
hide:
    - navigation
---

# Installation

Lungo is built upon [Docker Compose](https://github.com/docker/compose). Before proceeding, please ensure that Docker is
installed on your machine.

Alternatively, you can use [Podman Compose](https://github.com/containers/podman-compose)
with [Podman](https://podman.io/). You can
also [use Docker Compose with Podman](https://fedoramagazine.org/use-docker-compose-with-podman-to-orchestrate-containers-on-fedora/).

For instructions on setting up these tools, please refer to their respective documentation.

## With pipx

The recommended way to install Lungo is with [pipx](https://pypa.github.io/pipx/):

```bash linenums="1" title="Terminal"
pipx install lungo-cli
```

## With pip

To install Lungo with pip, run:

```bash linenums="1" title="Terminal"
pip install lungo-cli
```

## From source

To install Lungo from source, run:

```bash linenums="1" title="Terminal"
git clone --recurse-submodules https://github.com/raymond-u/lungo
cd lungo
pip install .
```
