# Changelog

All notable changes to gmshparser will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- MkDocs documentation system with Material theme
- Comprehensive user guide and developer guide
- API reference with mkdocstrings
- Test data organization in `testdata/` directory
- Git LFS support for large test files
- Quad visualization helpers (`get_quads`, `get_elements_2d`)

### Changed

- Migrated documentation from RST to Markdown
- Organized test data into `testdata/simple/`, `testdata/complex/`, `testdata/large/`
- Updated dev dependencies: black 24.x, flake8 7.x, matplotlib 3.10

### Removed

- Old RST documentation files
- setup.py (Poetry-only now)
- data/ directory (moved to testdata/)

## [0.2.0] - 2025-11-16

### Added

- Support for MSH 1.0 format (legacy `$NOD`/`$ELM` sections)
- Support for MSH 2.0, 2.1, 2.2 formats
- Support for MSH 4.0, 4.1 formats
- Automatic version detection
- Version-specific parser routing
- `VersionManager` for version validation
- V1 parsers (`NodesParserV1`, `ElementsParserV1`)
- V2 parsers (`NodesParserV2`, `ElementsParserV2`)
- Comprehensive test suite (34 tests, 97% coverage)
- Test files for all supported versions
- Quad visualization support
- Helper functions: `get_quads()`, `get_elements_2d()`

### Changed

- Updated to Python 3.8.1+ requirement
- Upgraded pytest to 8.0+
- Improved error messages

### Fixed

- MSH 1.0 parsing compatibility
- Version detection for legacy formats

## [0.1.0] - 2020-XX-XX

### Added

- Initial release
- MSH 4.1 format support
- Basic mesh parsing functionality
- Command-line interface
- Triangle visualization helpers

## Links

- [PyPI Releases](https://pypi.org/project/gmshparser/#history)
- [GitHub Releases](https://github.com/ahojukka5/gmshparser/releases)
- [GitHub Commits](https://github.com/ahojukka5/gmshparser/commits)
