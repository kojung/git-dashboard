# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Ability to exclude directories

### Changed

- Updated screenshot to latest

## [0.1.11] - 2022/04/24

### Added
- Command line mode where repo status are returned as JSON

## [0.1.10] - 2022/04/10

### Fixed
- Deal with invalid directory names gracefully (instead of just crashing)

### Added
- Added status bar and refresh button

### Changed
- Increased default refresh rate to 60 seconds

## [0.1.9] - 2022/04/02

### Fixed
- Moved git repo status update to a background thread to prevent unresponsive GUI

## [0.1.8] - 2022/03/27

### Changed
- Replaced with a cheaper/faster way of counting untracked files

## [0.1.7] - 2022/03/13

### Changed
- Make status column stretched

## [0.1.6] - 2022/03/06

### Added
- Added Changelog
- Added detailed status: ahead, behind, untracked, staged, clean/dirty
- Added -s option to scale fonts

### Changed
- Removed path column and replaced with tooltips

## [0.1.5]

### Fixed
- Removed pathlib from requirements

## [0.1.4]

### Added
- Added support for Mac OS.

### Fixed
- Avoid inaccessible folder.

### Changed
- Skip symlinks

## [0.1.3]

### Added
- First PyPi release

## [0.1.2]

### Added
- Test release

## [0.1.1]

### Added
- Test release

## [0.1.0]

### Added
- Initial release
