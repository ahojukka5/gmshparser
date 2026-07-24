# Contributing

Thank you for contributing to gmshparser.

## Report bugs and suggest features

Open a GitHub issue and include:

- a clear description of the problem or proposed feature
- steps to reproduce the problem
- expected and actual behavior
- Python version and operating system
- a small mesh file when relevant

## Set up the development environment

Fork and clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/gmshparser.git
cd gmshparser
```

Install the default development groups, which contain testing and quality tools:

```bash
uv sync
```

Install additional groups only when needed:

```bash
uv sync --group docs
uv sync --group benchmark
uv sync --group visualization
uv sync --all-groups
```

Dependency lock files are intentionally local and are not committed to this repository.

## Development workflow

Create a branch:

```bash
git checkout -b feature/your-feature-name
```

Run the complete local quality checks:

```bash
uv run ruff format --check gmshparser tests examples benchmarks
uv run ruff check gmshparser tests examples benchmarks
uv run pytest
```

Apply formatting and safe automatic lint fixes when necessary:

```bash
uv run ruff check --fix gmshparser tests examples benchmarks
uv run ruff format gmshparser tests examples benchmarks
```

Run an individual test:

```bash
uv run pytest tests/test_helpers.py::test_get_triangles
```

Generate an HTML coverage report:

```bash
uv run pytest --cov=gmshparser --cov-report=html
```

Run the parser performance baseline:

```bash
uv sync --no-default-groups --group benchmark
uv run --no-sync python -m benchmarks.run
```

See [Performance Benchmarks](benchmarks.md) for the measured phases and valid
comparison rules.

## Dependency groups

The groups in `pyproject.toml` have distinct purposes:

| Group | Purpose |
| --- | --- |
| `benchmark` | NumPy dependency used by the reproducible benchmark matrix |
| `test` | pytest and coverage tooling |
| `lint` | Ruff formatting and linting |
| `docs` | MkDocs documentation toolchain |
| `visualization` | matplotlib examples |
| `dev` | the default combination of `test` and `lint` |

Add dependencies to the narrowest suitable group:

```bash
uv add --group benchmark PACKAGE
uv add --group test PACKAGE
uv add --group lint PACKAGE
uv add --group docs PACKAGE
uv add --group visualization PACKAGE
```

Remove the generated `uv.lock` before committing if `uv` creates it locally.

## Coding standards

- Follow PEP 8.
- Use Ruff for formatting and linting.
- Keep all configured Ruff rules clean.
- Add type hints where they improve clarity.
- Write tests for new behavior and bug fixes.
- Document public APIs and user-visible changes.

## Documentation

Build the documentation:

```bash
uv sync --group docs
uv run mkdocs build
```

Serve it locally:

```bash
uv run mkdocs serve
```

## Continuous integration

GitHub Actions separates validation into these workflows and jobs:

- `quality` runs Ruff once on Python 3.12
- `test` runs pytest on Python 3.12, 3.13, and 3.14
- `package` builds and smoke-tests the wheel and source distribution after the
  quality and test jobs succeed
- **Parser benchmarks** records elapsed-time and memory artifacts for
  benchmark-related pull requests without fixed performance thresholds

Documentation is built on pull requests. Pushes to `master` additionally upload
and deploy the generated site with GitHub's official Pages actions.

## Pull requests

Before submitting a pull request, verify that:

- all tests pass
- `ruff format --check` reports no changes
- `ruff check` reports no violations
- documentation is updated when behavior changes
- the pull request explains what changed, why, and how it was tested

## Release process

For maintainers:

1. Update the version in `pyproject.toml` and `gmshparser/__init__.py`.
2. Update the changelog.
3. Build locally with `uv build --no-sources`.
4. Create and publish the GitHub release.
5. The release workflow builds and smoke-tests both distributions.
6. `uv publish` obtains a short-lived PyPI credential through GitHub OIDC.

The PyPI project must have a trusted publisher matching:

- owner: `ahojukka5`
- repository: `gmshparser`
- workflow: `python-publish.yml`
- environment: `pypi`

No PyPI token is stored in GitHub after trusted publishing is configured.

A manual publication can still be performed from an authorized local environment:

```bash
uv build --no-sources
uv publish
```

## License

By contributing, you agree that your contribution is licensed under the MIT License.
