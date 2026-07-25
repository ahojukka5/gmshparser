# Testing Guide

The repository uses pytest, pytest-cov, and Ruff through uv dependency groups.
Ruff handles both formatting and linting.

## Install the development environment

```bash
uv sync
```

The default `dev` group includes the `test` and `lint` groups.

## Run the suite

```bash
uv run pytest
```

The default pytest options in `pyproject.toml` enable verbose output and terminal
coverage reporting.

Run one module or test:

```bash
uv run pytest tests/test_helpers.py
uv run pytest tests/test_helpers.py::test_get_triangles
```

Generate an HTML coverage report:

```bash
uv run pytest --cov=gmshparser --cov-report=html
```

Open `htmlcov/index.html` in a browser.

## Formatting and linting

Run the same checks as the CI quality job:

```bash
uv run ruff format --check gmshparser tests examples
uv run ruff check gmshparser tests examples
```

Apply safe automatic fixes and formatting with:

```bash
uv run ruff check --fix gmshparser tests examples
uv run ruff format gmshparser tests examples
```

Run the coverage command used by the CI test job:

```bash
uv run pytest --cov=gmshparser --cov-report=xml --cov-report=term
```

## Test data

Mesh fixtures live under `testdata/`. They include simple version-specific
meshes and more complex files collected for regression testing. Tests should
refer to files that are committed to the repository rather than describing or
assuming uncommitted benchmark datasets.

See [Test Data](https://github.com/ahojukka5/gmshparser/blob/master/testdata/README.md) for the current organization.

## Writing tests

A parser test should verify the behavior that callers observe:

```python
import gmshparser


def test_mesh_version_and_counts():
    mesh = gmshparser.parse("testdata/simple/testmesh_v2_0.msh")

    assert mesh.get_version() == 2.0
    assert mesh.get_number_of_nodes() == 6
    assert mesh.get_number_of_elements() == 2
```

For new behavior:

- add the smallest useful mesh fixture
- verify public API results, not only internal implementation details
- cover malformed or unsupported input when relevant
- keep documentation examples consistent with the tested API

## Continuous integration

GitHub Actions runs Ruff once in a dedicated quality job, pytest on Python 3.12,
3.13, and 3.14, and distribution builds plus package smoke tests after those jobs
succeed. The documentation workflow builds MkDocs separately and deploys only on
pushes to `master`.

Exact test counts and coverage percentages change over time. The current CI run
and Codecov report are the authoritative results.
