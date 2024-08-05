# Configuring settings

## Location of configuration files

Lungo utilizes two configuration files: `config.yaml`, which contains general settings, and `users.yaml`, dedicated to
user management. By default, these files are located in a platform-dependent directory, such as `~/.config/lungo/` on
Linux. You can override this location by passing the `--config-dir` option to Lungo.

## Editing settings

A minimal `config.yaml` file looks like this:

```yaml linenums="1" title="config.yaml"
directories:
    users_dir: /home/lungo/users

network:
    base_url: https://lungo.com/

smtp:
    host: smtp.gmail.com
    port: 587
    username: joe
    password: joe123
    name: Lungo
    sender: joe@gmail.com
```

For a comprehensive list of available settings, please refer to
the [reference for config.yaml](../configuration/reference-for-config-yaml.md)
and [reference for users.yaml](../configuration/reference-for-users-yaml.md).

## Verifying settings

You can verify the correctness of your configuration files by running:

```bash linenums="1" title="Terminal"
lungo check
```

## Applying changes

After making any changes to the `config.yaml` file, you need to restart the Lungo service for the changes to take
effect.
