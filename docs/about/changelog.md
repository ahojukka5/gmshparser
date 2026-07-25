# Changelog

Notable user-visible changes to gmshparser are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and the project uses
semantic versioning.

## [Unreleased]

### Added

- Pythonic `gmshparser.read()` entry point for paths and open text streams
- explicit modern `gmshparser.api.parse()` alias while preserving top-level
  `gmshparser.parse()` as the unchanged compatibility entry point
- immutable modern mesh, node, element, entity, physical-group, collection, and
  version value objects in `gmshparser.api`
- physical group names and assignments from MSH 1.x, 2.x, and 4.x
- physical group lookup by name or `(dimension, tag)`, resolving its entities,
  elements, and participating nodes
- flat tag-addressable node and element collections with filtering by element
  type, dimension, entity, physical tag, and parametric status
- direct element-to-node object relationships
- unified `mesh.entities` view combining legacy node and element blocks
- `mesh.entity()`, `mesh.physical_group()`, and dimension views for points,
  curves, surfaces, and volumes
- centralized element type registry for numeric IDs 1–31 and 92–93 with
  family, dimension, polynomial order, connectivity size, primary-node count,
  and complete/incomplete metadata
- descriptive `ElementType` integer enum that keeps unknown numeric values
  representable without silently inferring their topology
- optional `gmshparser.numpy` interoperability with detached point arrays,
  original node tags, node entity keys, and element-type-specific cell blocks
- zero-based NumPy connectivity with original Gmsh node and element tags retained
  for round-trip identification
- structured `GmshError` and `ParseError` hierarchy with source filename, line
  number, section, and offending line attributes
- explicit errors for unsupported versions, binary input, unexpected EOF,
  malformed sections, nodes, elements, connectivity, and unknown element types
- reproducible MSH 2.2 and 4.1 parser benchmarks with elapsed-time, Python
  allocation, and process RSS reporting for legacy, modern, and NumPy paths
- a GitHub Actions benchmark workflow that uploads JSON and Markdown reports
  without enforcing noisy fixed performance thresholds
- separate Cartesian and parametric node coordinates
- PEP 621 console-script metadata for the installed `gmshparser` command
- `gmshparser --version` support
- wheel and source-distribution smoke tests for the installed CLI
- PyPI trusted publishing through GitHub OIDC

### Changed

- added MSH 2.x and 4.x `$Periodic` parsing with immutable modern periodic-link
  values and compatibility-model accessors
- made `gmshparser.read()` build immutable modern values through a dedicated
  `ModernMeshBuilder` without constructing a compatibility `Mesh`
- made version-specific node and element parsers emit raw blocks through a shared
  parser-target protocol while preserving the compatibility `parse()` API
- retained `Mesh.from_legacy()` as an explicit supported conversion without using
  it in the normal modern-reader path
- made `Element.element_type` the canonical modern attribute while retaining
  `Element.type` as an alias
- unified MSH 1.x, 2.x, and 4.x dimension and connectivity validation around the
  centralized element registry
- made section parsers validate declared record counts and consume their own
  `$End...` markers
- made legacy `parse()` and modern `read()` expose the same parser error types
- made legacy element-block lookup accept an optional element type while
  retaining two-argument lookup for unambiguous entities
- exported modern value and collection types at package level while retaining
  `gmshparser.Mesh` as the original compatibility class
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
- extended Ruff checks to benchmark sources
- separated CI into quality, test-matrix, and package jobs
- replaced the third-party Pages branch publisher with GitHub's official Pages
  artifact and deployment actions

### Fixed

- implemented the actual MSH 4.0 `$Entities`, `$Nodes`, `$Elements`, and
  `$Periodic` layouts instead of interpreting those sections as MSH 4.1
- rejected duplicate MSH 4 entity tags, non-finite or inverted geometry, and
  non-positive physical tags
- made `PhysicalGroupCollection.get()` return its default only for missing
  keys while preserving `KeyError` for ambiguous physical-group names
- preserved multiple element-type blocks on the same MSH 1.x or 2.x entity
  instead of overwriting all but the last type
- removed parser-side failure printing to stdout
- rejected binary MSH files before attempting to parse ASCII sections
- reported truncated and malformed records as contextual parser errors instead of
  leaking incidental `IndexError` and conversion failures
- synchronized `gmshparser.__version__` with package version 0.3.1
- restored the packaged CLI entry point in `pyproject.toml`
- removed incorrect claims that binary MSH files or Git LFS are supported

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
