# Prerequisites

## Running rootless containers

To ensure enhanced security, it is recommended to run Lungo in a non-root user environment. To achieve this, the
administrator needs to perform specific configurations as outlined in
the [Docker guide](https://docs.docker.com/engine/security/rootless/) or
the [Podman guide](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md).

To allow non-root users to bind to ports below 1024, you can utilize the `setcap` command:

```bash linenums="1" title="Terminal"
sudo setcap 'cap_net_bind_service=+ep' "$(command -v lungo)"
```

Alternatively, you can modify the value of `net.ipv4.ip_unprivileged_port_start` using the following command:

```bash linenums="1" title="Terminal"
# This will allow any user to bind to port 80
sudo sysctl net.ipv4.ip_unprivileged_port_start=80
```

## File permissions

In a rootless environment, proper file permissions must be set to enable non-root users on the host machine to read and
write files created from within the container, and vice versa. It is recommended to create a dedicated user for Lungo
and a group for sharing files between the container and the host. The following commands demonstrate this process:

```bash linenums="1" title="Terminal"
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

For more information on file permissions in a rootless environment, you can refer to
the [documentation](https://github.com/containers/podman/blob/main/troubleshooting.md#34-container-creates-a-file-that-is-not-owned-by-the-users-regular-uid).

Avoid using `sudo su lungo` to switch to the `lungo` user when launching Lungo in a rootless environment,
as it [may lead to improper functioning](https://www.redhat.com/sysadmin/sudo-rootless-podman). Instead, set a password
for the `lungo` user and log in normally:

```bash linenums="1" title="Terminal"
sudo chpasswd <<<'lungo:<password>'
```

## Firewall settings

Depending on your firewall configuration, you might need to allow access to ports 80 and 443, or any other ports that
you intend to use for HTTP and HTTPS. If you are using UFW (Uncomplicated Firewall), you can use the following commands:

```bash linenums="1" title="Terminal"
sudo ufw allow http
sudo ufw allow https
```

Please make sure to adjust the firewall settings according to your specific needs and security requirements.
