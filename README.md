# Lungo

Lungo is a comprehensive home lab setup designed specifically for academic research purposes.
Deployable on a single machine, it offers secure access to a range of services through a unified single sign-on portal.

## Featured services

- [Nginx](https://nginx.org/) as a reverse proxy
- [Authelia](https://www.authelia.com/) as a single sign-on portal
- [File Browser](https://filebrowser.org/) as a file manager
- [R Studio](https://posit.co/products/open-source/rstudio-server/) as an IDE for R

## Getting started

### Prerequisites

Lungo is built upon [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).
Please ensure they are installed on your machine.

Alternatively, you can use [Podman](https://podman.io/)
and [Podman Compose](https://github.com/containers/podman-compose).
For installation instructions, refer to their respective documentation.

### Rootless execution

For enhanced security, Lungo should be run in a non-root user environment. To do so, the administrator must
complete necessary configurations, as described in the [Docker guide](https://docs.docker.com/engine/security/rootless/)
or the [Podman guide](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md).

To enable non-root users to bind to port 80, modify the value of `net.ipv4.ip_unprivileged_port_start`
using the following command:

```bash
sudo sysctl net.ipv4.ip_unprivileged_port_start=80
```

In a rootless environment, permissions need to be configured to allow non-root users to read and write files
created by the containers. We recommend creating a dedicated user for Lungo and a group for sharing files
between containers and the host. The following commands illustrate this process:

```bash
# Create a group for sharing files
sudo groupadd share

# Create a user for Lungo
sudo useradd -m -g share lungo

# Add existing users to the group
sudo usermod -a -G share <username>

# Create a directory for shared files
sudo mkdir /home/shared
sudo chown lungo:share /home/shared
sudo chmod g+s /home/shared

# Create a directory for read-only shared files
sudo mkdir /home/shared_readonly
```

Ensure that the directories `/home/shared` and `/home/shared_readonly` are created before running Lungo,
as they will be mounted as volumes in the containers. If necessary, they can be symbolic links to other directories.

Avoid using `sudo su lungo` to switch to the `lungo` user when launching Lungo in a rootless environment,
as it [may not function properly](https://www.redhat.com/sysadmin/sudo-rootless-podman). Instead, set a password for
the `lungo` user to log in without root privileges:

```bash
sudo chpasswd <<<'lungo:<password>'
```

### Installation

The easiest way to install Lungo is via pip:

```bash
pip install lungo-cli
```

To install from source, clone the repository and run:

```bash
poetry install --compile
```

### Configuration

Before first use, Lungo requires some configuration. This can be done by running:

```bash
lungo init
```

To add a new user, run:

```bash
lungo user add <username>
```

If the user does not exist on the host machine, it must be created. To do so, run:

```bash
sudo useradd -m -G share <username>
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
