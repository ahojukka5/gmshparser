# Test Results

gmshparser is tested against committed mesh fixtures covering the supported MSH
version families and several element types.

## Current automated checks

GitHub Actions separates validation into dedicated jobs.

The quality job runs once on Python 3.12:

```bash
uv sync --no-default-groups --group lint
uv run --no-sync ruff format --check gmshparser tests examples
uv run --no-sync ruff check gmshparser tests examples
```

The test matrix runs on Python 3.12, 3.13, and 3.14:

```bash
uv sync --no-default-groups --group test
uv run --no-sync pytest --cov=gmshparser --cov-report=xml --cov-report=term
```

After quality and tests succeed, a separate package job builds the wheel and
source distribution and smoke-tests the installed package and CLI. The release
workflow repeats those package checks before publishing through PyPI trusted
publishing.

The documentation workflow installs only the `docs` dependency group and runs:

```bash
uv sync --no-default-groups --group docs
uv run --no-sync mkdocs build
```

Pull requests validate the documentation build. Pushes to `master` additionally
upload and deploy the site using GitHub's official Pages actions.

## Format coverage

Fixtures and parser tests cover:

- MSH 1.0 legacy `$NOD` and `$ELM` sections
- MSH 2.0, 2.1, and 2.2 node and element layouts
- MSH 2.x element records containing tags
- MSH 4.0 and 4.1 entity-block node and element layouts
- unsupported-version and version-management behavior

The current data model does not expose complete physical-name or physical-tag
metadata, so the presence of such tags in a fixture should not be described as
full physical-group support.

## Element and helper coverage

The suite exercises multiple element dimensions and types, including points,
lines, triangles, quadrangles, and tetrahedra. It also tests the CLI and the
visualization helper return values.

## Running tests locally

```bash
uv sync
uv run pytest
```

Run one module:

```bash
uv run pytest tests/test_helpers.py
```

Generate an HTML coverage report:

```bash
uv run pytest --cov=gmshparser --cov-report=html
```

## Authoritative status

Mesh files are stored under `testdata/`; see
[`testdata/README.md`](../../testdata/README.md).

Exact test counts and coverage percentages change as the project evolves. The
GitHub Actions result and Codecov report for the current commit are the
authoritative status rather than numbers copied into documentation.
