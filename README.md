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
  A home lab setup for small-to-mid-scale private on-premises deployments,
  <br>
  with everything configurable in human-readable YAML files.
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

- Fully configurable via YAML files - everything including user management
- Easy interoperability - single sign-on portal to access all applications
- Batteries-included - comes with a variety of applications out of the box
- Secure by default - is designed to be run in a non-root user environment

## Installation

The easiest way to install Lungo is via pip:

```bash
pip install lungo-cli
```

To install from source, run:

```bash
git clone --recurse-submodules https://github.com/raymond-u/lungo
cd lungo
poetry install --compile
```

## Getting started

### Prerequisites

Lungo is built upon [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).
Please ensure they are installed on your machine.

Alternatively, you can use [Podman](https://podman.io/)
and [Podman Compose](https://github.com/containers/podman-compose).

For installation instructions, please refer to their respective documentation.

### Rootless execution

For enhanced security, Lungo should be run in a non-root user environment. To do so, the administrator must
complete necessary configurations, as described in the [Docker guide](https://docs.docker.com/engine/security/rootless/)
or the [Podman guide](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md).

To enable non-root users to bind to port 80, run:

```bash
sudo setcap 'cap_net_bind_service=+ep' "$(command -v lungo)"
```

Or you can modify the value of `net.ipv4.ip_unprivileged_port_start` using the following command:

```bash
# This will allow any user to bind to port 80
sudo sysctl net.ipv4.ip_unprivileged_port_start=80
```

In a rootless environment, permissions need to be configured to allow non-root users on the host machine to
read and write files created by the container, and vice versa. We recommend creating a dedicated user for Lungo
and a group for sharing files between the container and the host. The following commands illustrate this process:

```bash
# Create a group for sharing files
sudo groupadd shared

# Create a dedicated user for Lungo
sudo useradd -m -g shared lungo

# Add an existing user to the group
sudo usermod -a -G shared <username>

# Create a directory for shared files
sudo mkdir /mnt/data/shared
sudo chown lungo:shared /mnt/data/shared
sudo chmod g+rws /mnt/data/shared
```

You can read more about file permissions in a rootless
environment [here](https://github.com/containers/podman/blob/main/troubleshooting.md#34-container-creates-a-file-that-is-not-owned-by-the-users-regular-uid).

Avoid using `sudo su lungo` to switch to the `lungo` user when launching Lungo in a rootless environment,
as it [may not function properly](https://www.redhat.com/sysadmin/sudo-rootless-podman). Instead, set a password for
the `lungo` user and log in normally:

```bash
sudo chpasswd <<<'lungo:<password>'
```

### Configuration

Lungo has two essential configuration files: `config.yaml`, which contains general settings,
and `users.yaml`, dedicated to user management. The default location for these files is platform-dependent,
e.g. `~/.config/lungo/` on Linux. You can override this location by passing the `--config-dir` option to Lungo.

For a full list of available settings, please refer to [config.yaml](src/lungo_cli/resources/excluded/config.yaml)
and [users.yaml](src/lungo_cli/resources/excluded/users.yaml). Also, you may find these [examples](examples) helpful.

You can verify the correctness of your configuration files by running:

```bash
lungo check
```

### Usage

To launch Lungo, just run:

```bash
lungo up
```

### Additional notes

You might need to configure your firewall to permit access on ports 80 and 443. For instance, if you're using UFW, run:

```bash
sudo ufw allow http
sudo ufw allow https
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
