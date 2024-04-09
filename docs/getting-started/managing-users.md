# Managing users

## Adding a user

To add a new user, add an entry to the `users.yaml` file. Here is an example of a minimal entry:

```yaml linenums="1" title="users.yaml"
accounts:
    -   username: joe
        name:
            first: Joe
            last: Doe
        email: joe@gmail.com
        role: user
```

The username and email must be unique across all users. Note that you don't need to specify a password for the user.
Instead, the user will use the password reset feature to set their own password.

A user can be assigned one of the following roles:

- `guest`
- `user`
- `admin`

Each role inherits the permissions of the previous one. For instance, a user with the `admin` role can perform all
actions that a `guest` or `user` can.

## About the `extra.user_dir` field

Every user has a dedicated directory for storing their files. By default, this directory is located within `users_dir`.
However, you can set the `extra.user_dir` field to specify a different location for a specific user. For instance:

```yaml hl_lines="5" linenums="1" title="users.yaml"
accounts:
    -   username: joe
    -   username: jane
        extra:
            user_dir: /mnt/data/jane
```

Suppose you have set `users_dir` to `/home/lungo/users` in your `config.yaml` file. In this case, the user `joe` will
have `/home/lungo/users/joe` as their user directory, while the user `jane` will have `/mnt/data/jane` as their user
directory.

## Removing a user

To remove a user, simply remove the corresponding entry from the `users.yaml` file. Alternatively, you can set
the `enabled` flag to `false` to disable the user without removing the entry.

## Applying changes

After making any changes to the `users.yaml` file, you need to restart the Lungo service for the changes to take effect.
