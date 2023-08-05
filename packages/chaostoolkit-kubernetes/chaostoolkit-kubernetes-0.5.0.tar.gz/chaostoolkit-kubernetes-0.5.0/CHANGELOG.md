# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.5.0...HEAD

## [0.5.0][] - 2017-12-06

[0.5.0]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.4.3...0.5.0

### Changed

- Updated to match chaostoolkit-lib 0.6.0 API changes
- Probes now return `True` on success so they can be nicely used from the
  steady state hypothesis checks

## [0.4.3][] - 2017-11-23

[0.4.3]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.4.2...0.4.3

### Changed

- Removing unwanted parameter

## [0.4.2][] - 2017-11-20

[0.4.2]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.4.1...0.4.2

### Changed

- Proper verify SSL reading of the environment key

## [0.4.1][] - 2017-11-20

[0.4.1]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.4.0...0.4.1

### Added

- Passing secrets down to client function


## [0.4.0][] - 2017-11-20

[0.4.0]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.3.0...0.4.0

### Added

- Can create a client from secrets


## [0.3.0][] - 2017-11-20

[0.3.0]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.2.0...0.3.0

### Added

- Can now authenticate to the Kubernetes API endpoint either via a token,
  username/password or certificate/pkey. All of this via environment variable.
  By default, still looks up for ~/kube/config if it exists


## [0.2.0][] - 2017-10-23

[0.2.0]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.1.1...0.2.0

### Added

- Remove check Kubernetes service by name

### Changed

-   Do not build a universal wheel package (no Python 2 support in chaostoolkit)

## [0.1.1][] - 2017-10-06

[0.1.1]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/compare/0.1.0...0.1.1

### Changed

-   Package up extra files when installed from source

## [0.1.0][] - 2017-10-06

[0.1.0]: https://github.com/chaostoolkit/chaostoolkit-kubernetes/tree/0.1.0

### Added

-   Initial release