# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Nightly](https://github.com/raymond-u/lungo/compare/v0.1.9...HEAD)

### Added

- Add a new option to rate limit requests per IP address

### Fixed

- Fix the outdated warning in the documentation
- Fix a bug where the lock file may persist if the container tool binary cannot be found

### Changed

- Migrate to pnpm

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
