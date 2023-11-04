# Allowing anonymous access

In addition to the three roles (`guest`, `user`, and `admin`) that can be assigned to a user, Lungo also supports
anonymous access, which is associated with the role `unregistered`. To enable anonymous access, you need to
configure the `unregistered.allowed_apps` field in the `config.yaml` file:

```yaml linenums="1" title="config.yaml"
rules:
    privileges:
        unregistered:
            allowed_apps:
                - privatebin
                - rstudio
```

To enable anonymous access for applications that typically require user accounts, such as RStudio, you must add a user
with the username `anonymous` in the `users.yaml` file:

```yaml linenums="1" title="users.yaml"
accounts:
    -   username: anonymous
        name:
            first: Anonymous
            last: User
        email: an@nymo.us
        role: guest
```

The user with the username `anonymous` serves as a shared account for anonymous access. The `name` and `email` fields
can be set to arbitrary values (although they must still be provided). The `role` field must be set to `guest` and
cannot be changed.
