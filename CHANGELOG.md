# Change Log
All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- `.travis.yml` file for CI testing.
- `setup.cfg` file for `flake8` testing.
- Http requests mock for testing.
- `league.status_code` for testing purposes.
- Exceptions for status codes.
- Tests for future development.

### Changed
- Deprecation warnings for `Team` class attributes. Next Version
will remove old attributes.
- README.md shows build status from Travis CI.
- Better documentation in README.md.
- Added range for dependencies.
- `from espnff import *` now only imports `League` and `Team`.


## [1.0.1] - 2016-10-18
### Added
- Tests for utility functions.

### Changed
- Output for matrix functions now lists instead of numpy array.

### Fixed
- Fix issue where not all teams showed in power rankings.
- Fix issue where power rankings output was not sorted.

## [1.0.0] - 2016-10-04
### Added
- New attributes for Teams.
- Started using Semantic Versioning.

### Changed
- Replaced urls with ESPN's private API url.
- Replaced `Members` class with `Teams`.
- `get_week` function now `power_rankings`
- Teams now accessable as list attribute in `League`.

### Removed
- `get_member`
- `get_all_members`

## 0.2.2 - 2016-09-27
### Fixed
- Fix issue where margin of victory calculation in the power rankings
algorithm accounted for 50% of the total power points. Should have been 5%.

## 0.2.1 - 2016-09-15
### Fixed
- Fix issue where scores from games that weren't played would become
a string character instead of an integer.

## 0.2.0 - 2016-07-03
### Changed
- Rearranged output for `get_week`.

## 0.1.0 - 2016-05-13
### Added
- Power rankings function `get_week` to `League` class.
- README information.
- `setup.py` to turn project into module.

### Changed
- Renamed `power_rankings.py` to `espnff.py`.

## 0.0.0 - 2016-05-12
### Added
- League and Members classes to obtain information about ESPN league.


[Unreleased]: https://github.com/rbarton65/espnff/compare/v1.0.0...HEAD
[1.0.1]: https://github.com/rbarton65/espnff/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/rbarton65/espnff/releases/tag/v1.0.0
