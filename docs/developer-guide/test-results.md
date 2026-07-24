# Test Results

gmshparser is tested against mesh files covering the supported MSH format families and multiple element types.

## Current automated checks

GitHub Actions runs the project on Python 3.12, 3.13, and 3.14. Every matrix job performs:

```bash
uv sync --no-default-groups --group test --group lint
uv run --no-sync black . --check
uv run --no-sync flake8 gmshparser tests
uv run --no-sync pytest --cov=gmshparser --cov-report=xml --cov-report=term
```

The documentation workflow separately installs only the `docs` dependency group and runs:

```bash
uv sync --no-default-groups --group docs
uv run --no-sync mkdocs build
```

This separation keeps test environments free of matplotlib and documentation tooling.

## Format coverage

The test data includes examples for:

- MSH 1.0 legacy `$NOD` and `$ELM` sections
- MSH 2.0, 2.1, and 2.2 node and element sections
- physical groups in MSH 2.x files
- MSH 4.0 and 4.1 entity-based node and element organization

## Element coverage

The suite exercises elements from zero to three dimensions, including:

- points
- lines
- triangles
- quadrangles
- tetrahedra

## Running tests locally

Install the default development environment:

```bash
uv sync
```

Run the full suite:

```bash
uv run pytest
```

Run one test module:

```bash
uv run pytest tests/test_helpers.py
```

Generate an HTML coverage report:

```bash
uv run pytest --cov=gmshparser --cov-report=html
```

## Test data organization

Mesh files are stored under `testdata/` and grouped by complexity and purpose. See [`testdata/README.md`](../../testdata/README.md) for details and contribution guidance.

Exact test and coverage totals change as the project evolves. The GitHub Actions result for the current commit is the authoritative status.
