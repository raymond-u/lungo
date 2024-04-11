# Managing plugins

## Listing plugins

You can view a list of both installable and installed plugins by running the following command:

```bash linenums="1" title="Terminal"
lungo list
```

## Installing a built-in plugin

By default, Lungo does not install any plugins. To install a built-in plugin, run the following command:

```bash linenums="1" title="Terminal"
lungo install <plugin>
```

## Installing a custom plugin

To install a custom plugin, create a `plugins` directory within the configuration directory, and place the plugin
directory inside it. For instance, if you want to install a plugin called `forfun` and you are using the default
configuration directory on Linux, put the plugin files inside `~/.config/lungo/plugins/forfun/`. After that, run the
following command:

```bash linenums="1" title="Terminal"
lungo install <plugin>
```

## Configuring a plugin

To configure settings specific to a plugin, include them in the `plugins` section of the `config.yaml` file. For
instance, to configure the `filebrowser` plugin, add the following settings:

```yaml linenums="1" title="config.yaml"
plugins:
    filebrowser:
        enabled: true
```

Please note that plugins are enabled by default upon installation, so explicit enabling is not necessary.

## Uninstalling a plugin

To uninstall an installed plugin, run the following command:

```bash linenums="1" title="Terminal"
lungo uninstall <plugin>
```

## Applying changes

After making any changes to the plugins, you need to restart the Lungo service for the changes to take effect.
