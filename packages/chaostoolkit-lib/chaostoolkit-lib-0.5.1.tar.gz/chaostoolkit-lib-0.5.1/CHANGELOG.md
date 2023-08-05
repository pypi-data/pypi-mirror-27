# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit/chaostoolkit-lib/compare/0.5.1...HEAD

## [0.5.1][] - 2017-11-23

[0.5.1]: https://github.com/chaostoolkit/chaostoolkit-lib/compare/0.5.0...0.5.1

### Changed

-   Do not shadow functions
-   Log full errors on debug level
-   Always pause even if activity failed


## [0.5.0][] - 2017-11-19

[0.5.0]: https://github.com/chaostoolkit/chaostoolkit-lib/compare/0.4.0...0.5.0

### Changed

-   Split the inner of `run_experiment` into various functions for better
    composability
-   Pause before/after activity


## [0.4.0][] - 2017-10-18

[0.4.0]: https://github.com/chaostoolkit/chaostoolkit-lib/compare/0.3.0...0.4.0

### Changed

-   Better logging

## [0.3.0][] - 2017-10-18

[0.3.0]: https://github.com/chaostoolkit/chaostoolkit-lib/compare/0.2.0...0.3.0

### Added

-   An `expected_status` for HTTP probe to consider HTTP errors as expected in
    some cases

## [0.2.0][] - 2017-10-10

[0.2.0]: https://github.com/chaostoolkit/chaostoolkit-lib/compare/0.1.1...0.2.0

### Added

-   A first draft to loading secrets from environment
-   Passing those secrets as a mapping to actions and probes expecting them
-   Added support for background activities
-   Dry mode support

### Removed

-   Unused layer module

## [0.1.1][] - 2017-10-06

[0.1.1]: https://github.com/chaostoolkit/chaostoolkit-lib/compare/0.1.0...0.1.1

### Changed

-   Package up extra files when installed from source

## [0.1.0][] - 2017-10-06

[0.1.0]: https://github.com/chaostoolkit/chaostoolkit-lib/tree/0.1.0

### Added

-   Initial release