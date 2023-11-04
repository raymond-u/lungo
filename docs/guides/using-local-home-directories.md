# Using local home directories

In the `config.yaml` file, you can find the `users_dir` field, which determines the storage location for user files. By
configuring this setting, you can map the home directories of local users to the corresponding location inside the
container.

```yaml linenums="1" title="config.yaml"
directories:
    users_dir: /home
```

To enable write access to directories owned by a local user from within the container, you must ensure that the UID
or GID of those directories matches the user running Lungo, and that appropriate write permissions have been granted.

For instance, consider a scenario where a directory is owned by the user `joe`, and Lungo is running with the
user `lungo`. In this case, the directory should be assigned to the same group as the primary group of `lungo`, and
group write permission should be granted. For more information, please refer to
the [file permissions](../getting-started/prerequisites.md#file-permissions) section.
