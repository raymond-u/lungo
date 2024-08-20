# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Nightly](https://github.com/raymond-u/lungo/compare/v0.5.9...HEAD)

### Fixed

- Allow popups in the web UI

## [0.5.9](https://github.com/raymond-u/lungo/compare/v0.5.8...v0.5.9) - 2024-8-6

### Added

- The `Volumes` top-level key in the plugin's compose file is now supported
- JupyterLab now comes with `git`, `less`, `nano`, and `vim` pre-installed
- RStudio now comes with `nano` pre-installed

### Changed

- The default session lifetime is now 48 hours
- The changes made to user home directories are now retained across container restarts in File Browser
- The changes made to user home directories are now retained across container restarts in JupyterLab
- The changes made to user home directories are now retained across container restarts in RStudio
- Update JupyterHub to 4.1.6
- Update Xray to 1.8.23

### Fixed

- Opening shared links from within File Browser no longer creates a new tab
- Opening shared links from within PrivateBin no longer results in a hanging loading screen
- Implement a workaround for a bug in Chrome that was preventing the text editor in File Browser from functioning
- Implement a workaround for a bug in Safari that was preventing RStudio from loading correctly

## [0.5.8](https://github.com/raymond-u/lungo/compare/v0.5.7...v0.5.8) - 2024-7-28

### Changed

- Allow passwordless sudo in JupyterLab
- Allow passwordless sudo in RStudio
- Update JupyterLab to 4.2.4
- Update PrivateBin to 1.7.4
- Update Xray to 1.8.21

### Fixed

- Websocket connections can now remain open for up to 1 hour
- Admin accounts can now use sudo in JupyterLab

## [0.5.7](https://github.com/raymond-u/lungo/compare/v0.5.6...v0.5.7) - 2024-6-27

### Fixed

- Check if the file exists before removing it

## [0.5.6](https://github.com/raymond-u/lungo/compare/v0.5.5...v0.5.6) - 2024-6-27

### Changed

- Update JupyterLab to 4.2.3

### Fixed

- Ensure the removal of the socket file during launch

## [0.5.5](https://github.com/raymond-u/lungo/compare/v0.5.4...v0.5.5) - 2024-6-26

### Changed

- Enable the access of the website using raw IP addresses
- Update Xray to 1.8.16

### Fixed

- Allow `plugins` in the configuration file to be omitted
- Prevent unnecessary downloads when rebuilding JupyterHub image

## [0.5.4](https://github.com/raymond-u/lungo/compare/v0.5.3...v0.5.4) - 2024-6-26

### Fixed

- Allow `plugins` in the configuration file to be omitted

## [0.5.3](https://github.com/raymond-u/lungo/compare/v0.5.2...v0.5.3) - 2024-6-25

### Fixed

- Disable rich markup when printing the output of shell commands

## [0.5.2](https://github.com/raymond-u/lungo/compare/v0.5.1...v0.5.2) - 2024-6-22

### Fixed

- Update user accounts correctly

## [0.5.1](https://github.com/raymond-u/lungo/compare/v0.5.0...v0.5.1) - 2024-6-22

### Fixed

- Generate Kratos secrets correctly

## [0.5.0](https://github.com/raymond-u/lungo/compare/v0.4.2...v0.5.0) - 2024-6-22

### Breaking Changes

- `network.hostname` has been replaced by `network.base_url` in the configuration file to support custom ports

### Changed

- Apply a margin to the apps in the web UI
- Simplify the output of `lungo list` command
- Update JupyterLab to 4.2.2
- Update RStudio to 4.4.1
- Update Stirling PDF to 0.26.1
- Update Xray to 1.8.15

### Fixed

- The console tab of File Browser is now working correctly

## [0.4.2](https://github.com/raymond-u/lungo/compare/v0.4.1...v0.4.2) - 2024-5-25

### Changed

- Increase the bandwidth limit for RustDesk
- Update File Browser to 2.30.0
- Update JupyterLab to 4.2.1
- Update RustDesk Server to 1.1.11-1
- Update Xray to 1.8.13

### Fixed

- Stream the output from the container tool to the console when verbose mode is enabled
- Always check the return code of the container tool

## [0.4.1](https://github.com/raymond-u/lungo/compare/v0.4.0...v0.4.1) - 2024-5-16

### Fixed

- Forward cookies set back to the backend in subsequent sequential requests
- Show incompatible plugins in the output of `lungo list`

## [0.4.0](https://github.com/raymond-u/lungo/compare/v0.3.0...v0.4.0) - 2024-5-15

### Breaking Changes

- `BasePlugin.config` has been renamed to `BasePlugin.manifest`
- `BasePlugin.get_render_context` has been renamed to `BasePlugin.get_custom_rendering_context`
- `BasePlugin.update_data` has been renamed to `BasePlugin.on_plugin_initialization`
- `compatible_with` is now a required field for plugins
- `version` is now a required field for plugins
- Custom variables in the rendering context provided by plugins are now located under the `plugin.custom` key

### Added

- Built-in RustDesk plugin
- Built-in Stirling PDF plugin
- Plugins can now perform custom actions before the rendering process
- Plugins can now specify a custom name for use in the web path
- Plugins can now specify binding ports on the host machine
- Additional variables are now accessible in the rendering context for plugins

### Changed

- Websocket connections can now remain open for up to 1 hour
- Update JupyterLab to 4.2.0
- Update PrivateBin to 1.7.3
- Update RStudio to 4.4.0
- Update Xray to 1.8.11

### Fixed

- Plugins can be correctly installed even if the directory name differs from the plugin name
- Render dropdown menus correctly for Safari on iOS
- Ensure that the required directories always exist

### Security

- Avoid including cookies managed by other services when making requests to the backend

## [0.3.0](https://github.com/raymond-u/lungo/compare/v0.2.3...v0.3.0) - 2024-4-15

### Breaking Changes

- Raise the minimum required version of Python to 3.12
- Built-in apps are now installed as plugins
- The `modules` configuration has been renamed to `plugins`
- Guest role and user role accounts no longer have access to apps by default

### Added

- New plugin system
- Allow login through a one-time code sent via email
- Allow control over the maximum size of the client request body
- CLI now streams shell command output when in development mode

### Changed

- Hide fullscreen button for narrow screen widths
- Update JupyterHub to 4.1.5
- Update JupyterLab to 4.1.6
- Update RStudio to 4.3.3
- Update Xray to 1.8.10

### Fixed

- Remove lock file when the service fails to start
- Fix the recurrent Nginx socket binding issue
- Remove an incorrect instruction from the documentation
- Do not recreate File Browser database file on every start

## [0.2.3](https://github.com/raymond-u/lungo/compare/v0.2.2...v0.2.3) - 2024-2-16

### Changed

- Allow containers to restart automatically after a crash
- Update File Browser to 2.27.0
- Update JupyterLab to 4.1.1
- Update PrivateBin to 1.7.1
- Update Xray to 1.8.7

## [0.2.2](https://github.com/raymond-u/lungo/compare/v0.2.1...v0.2.2) - 2023-11-27

### Changed

- Remove the user's last name from the greeting in the web UI
- Redirect stderr to stdout to avoid formatting issues in the CLI

## [0.2.1](https://github.com/raymond-u/lungo/compare/v0.2.0...v0.2.1) - 2023-11-26

### Fixed

- Fix the permission issue during data migration
- Update bundled resources when version changes

## [0.2.0](https://github.com/raymond-u/lungo/compare/v0.1.12...v0.2.0) - 2023-11-26

### Added

- Add the Xray module
- Add fullscreen mode for the web UI
- Add theme selector for the web UI

### Changed

- Update JupyterLab to 4.0.9

### Fixed

- Show error messages correctly in the web UI
- Correct handling of redirects when using non-standard ports
- Include the port number in the forwarded `Host` header

## [0.1.12](https://github.com/raymond-u/lungo/compare/v0.1.11...v0.1.12) - 2023-11-22

### Added

- Add description for `Too Many Requests` errors in the web UI

### Fixed

- Perform case-insensitive matching for the `Upgrade` header
- Handle websocket connections correctly
- Fix the resend button in the web UI
- Remove border color of the `input` element in the web UI
- Fix a bug that causes email delivery failures

### Security

- Use custom Lua code for authentication to prevent endpoint probing

## [0.1.11](https://github.com/raymond-u/lungo/compare/v0.1.10...v0.1.11) - 2023-11-19

### Added

- Support user-defined trusted proxies

### Changed

- Optimize the web UI layout for narrow screen widths

### Fixed

- Check if the port is available before starting the container
- Fix a bug where URL search parameters are not passed to the backend

## [0.1.10](https://github.com/raymond-u/lungo/compare/v0.1.9...v0.1.10) - 2023-11-14

### Added

- Add a new option to protect sensitive API endpoints from brute force attacks
- Support Docker Compose with Podman backend

### Changed

- Migrate to pnpm

### Fixed

- Fix the outdated warning in the documentation
- Fix a bug where the lock file may persist if the container tool binary cannot be found
- Hide the navigation rail when there is no app to display

## [0.1.9](https://github.com/raymond-u/lungo/compare/v0.1.8...v0.1.9) - 2023-11-7

### Changed

- Update File Browser to 2.26.0
- Update JupyterLab to 4.0.8
- Update RStudio to 4.3.2

### Fixed

- Do not print local variables in panic messages

## [0.1.8](https://github.com/raymond-u/lungo/compare/v0.1.7...v0.1.8) - 2023-11-5

### Fixed

- Fix the GitHub Actions workflow

## [0.1.7](https://github.com/raymond-u/lungo/compare/v0.1.6...v0.1.7) - 2023-11-4

### Added

- Add logging to Keto, Kratos, and Oathkeeper
- Documentation

### Fixed

- Do not pass anonymous account to Kratos

## [0.1.6](https://github.com/raymond-u/lungo/compare/v0.1.5...v0.1.6) - 2023-10-25

### Fixed

- Correct the use of padding in email template styles

## [0.1.5](https://github.com/raymond-u/lungo/compare/v0.1.4...v0.1.5) - 2023-10-25

### Fixed

- Make Nginx handle encoded URL paths correctly

## [0.1.4](https://github.com/raymond-u/lungo/compare/v0.1.3...v0.1.4) - 2023-10-25

### Fixed

- Set Bash as the default shell in the container
- Make Nginx handle encoded URL paths correctly

## [0.1.3](https://github.com/raymond-u/lungo/compare/v0.1.2...v0.1.3) - 2023-10-24

### Fixed

- Make CI to check out submodules correctly when building the image

## [0.1.2](https://github.com/raymond-u/lungo/compare/v0.1.1...v0.1.2) - 2023-10-24

### Fixed

- Prevent the here-documents syntax that is not supported by Podman
- Use way less layers when building the image

## [0.1.1](https://github.com/raymond-u/lungo/compare/v0.1.0...v0.1.1) - 2023-10-24

### Added

- Use GitHub Actions for publishing to PyPI

## [0.1.0](https://github.com/raymond-u/lungo/releases/tag/v0.1.0) - 2023-10-24

Initial release
