# Changelog

Notable user-visible changes to gmshparser are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and the project uses
semantic versioning.

## [Unreleased]

### Added

- Pythonic `gmshparser.read()` entry point for paths and open text streams
- immutable modern mesh, node, element, entity, collection, and version value
  objects in `gmshparser.api`
- flat tag-addressable node and element collections with filtering by element
  type, dimension, entity, and parametric status
- direct element-to-node object relationships
- unified `mesh.entities` view combining legacy node and element blocks
- descriptive `ElementType` integer enum with support for unnamed numeric types
- separate Cartesian and parametric node coordinates
- PEP 621 console-script metadata for the installed `gmshparser` command
- `gmshparser --version` support
- wheel and source-distribution smoke tests for the installed CLI
- PyPI trusted publishing through GitHub OIDC

### Changed

- made visualization helpers accept both the modern `read()` model and the
  compatibility `parse()` model
- corrected README, user-guide, API, architecture, testing, and test-data
  documentation to match the current implementation
- documented Python 3.12+, ASCII-only parsing, version-specific parser routing,
  and the actual helper return values
- pointed MkDocs site metadata and badges to GitHub Pages
- replaced stale exact test-count and coverage claims with links to CI and
  Codecov as the authoritative status
- replaced Black and flake8 with Ruff for formatting and linting
- enabled Ruff bugbear, import-sorting, and pyupgrade checks and modernized
  imports, type annotations, string formatting, and loop variables accordingly
- separated CI into quality, test-matrix, and package jobs
- replaced the third-party Pages branch publisher with GitHub's official Pages
  artifact and deployment actions

### Fixed

- synchronized `gmshparser.__version__` with package version 0.3.1
- restored the packaged CLI entry point in `pyproject.toml`
- removed incorrect claims that binary MSH files, complete physical-group
  metadata, or Git LFS are currently supported

## [0.3.1]

### Changed

- migrated project builds and development workflows from Poetry to uv and
  `uv_build`
- raised the supported Python requirement to 3.12 or newer
- updated CI to test Python 3.12, 3.13, and 3.14
- grouped development dependencies with PEP 735 dependency groups
- intentionally stopped committing dependency lock files
- modernized GitHub Actions and package build smoke tests

### Documentation

- added the MkDocs Material documentation site
- organized user, developer, API, and test-data documentation
- added triangle, quadrilateral, and mixed-2D visualization guidance

## [0.2.0] - 2025-11-16

### Added

- MSH 1.0 support for legacy `$NOD` and `$ELM` sections
- MSH 2.0, 2.1, and 2.2 node and element parsing
- MSH 4.0 and 4.1 node and element parsing
- automatic version detection and version-specific parser routing
- `VersionManager`, V1 parsers, and V2 parsers
- quadrilateral and mixed-2D helper functions
- version-specific test fixtures

### Fixed

- MSH 1.0 parsing compatibility
- version detection for legacy formats

## [0.1.0]

### Added

- initial mesh parser
- MSH 4.1 parsing
- Python API
- command-line helpers
- triangle visualization helper

## Links

- [PyPI releases](https://pypi.org/project/gmshparser/#history)
- [GitHub releases](https://github.com/ahojukka5/gmshparser/releases)
- [GitHub commits](https://github.com/ahojukka5/gmshparser/commits)
