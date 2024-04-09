<br>

<h1 align="center">
  <a href="https://github.com/raymond-u/lungo">
      <img src="https://github.com/raymond-u/lungo/assets/36328498/5a8a3696-61c1-46cc-a1b4-144141da2d36" alt="Lungo" width="120">
  </a>
  <br>
  <b>Lungo</b>
  <br>
</h1>

<p align="center">
  A user-friendly home lab setup designed for small-to-mid-scale on-premises hosting.
  <br>
</p>

<p align="center">
  <a href="https://pypi.org/project/lungo-cli/" style="text-decoration: none">
    <img src="https://badge.fury.io/py/lungo-cli.svg" alt="PyPI version">
  </a>
  <a href="https://opensource.org/licenses/MIT" style="text-decoration: none">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
</p>

<br>

## Features

- **Complete configurability** - manage everything declaratively through YAML files
- **Seamless interoperability** - access all applications via a single sign-on portal
- **Batteries included** - extend functionality with both built-in and custom plugins
- **Containerized solution** - designed to operate in a rootless Docker environment
- **Security by default** - use HTTPS and secure server settings across the system

## Installation

The recommended way to install Lungo is via [pipx](https://pypa.github.io/pipx/):

```bash
pipx install lungo-cli
```

Note that Lungo is built upon [Docker Compose](https://github.com/docker/compose). Before proceeding, please ensure that
Docker is installed on your machine.

Alternatively, you can use [Podman Compose](https://github.com/containers/podman-compose)
with [Podman](https://podman.io/). You can
also [use Docker Compose with Podman](https://fedoramagazine.org/use-docker-compose-with-podman-to-orchestrate-containers-on-fedora/).

For instructions on setting up these tools, please refer to their respective documentation.

## Quickstart

Copy the example configuration files to the platform-specific configuration directory. For example, on Linux, you can
use the following command:

```bash
mkdir -p ~/.config/lungo
cp examples/* ~/.config/lungo
```

Edit the configuration files according to your preferences. Then, launch the Lungo service by running the following
command:

```bash
lungo up
```

## Documentation

For more information, please refer to the [documentation](https://raymond-u.github.io/lungo/).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
