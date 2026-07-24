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

Install the default development groups, which contain testing and linting tools:

```bash
uv sync
```

Install additional groups only when needed:

```bash
uv sync --group docs
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
uv run black gmshparser tests examples --check
uv run flake8 gmshparser tests
uv run pytest
```

Apply formatting when necessary:

```bash
uv run black gmshparser tests examples
```

Run an individual test:

```bash
uv run pytest tests/test_helpers.py::test_get_triangles
```

Generate an HTML coverage report:

```bash
uv run pytest --cov=gmshparser --cov-report=html
```

## Dependency groups

The groups in `pyproject.toml` have distinct purposes:

| Group | Purpose |
| --- | --- |
| `test` | pytest and coverage tooling |
| `lint` | formatting and static checks |
| `docs` | MkDocs documentation toolchain |
| `visualization` | matplotlib examples |
| `dev` | the default combination of `test` and `lint` |

Add dependencies to the narrowest suitable group:

```bash
uv add --group test PACKAGE
uv add --group lint PACKAGE
uv add --group docs PACKAGE
uv add --group visualization PACKAGE
```

Remove the generated `uv.lock` before committing if `uv` creates it locally.

## Coding standards

- Follow PEP 8.
- Use Black for formatting.
- Keep flake8 clean.
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

## Pull requests

Before submitting a pull request, verify that:

- all tests pass
- Black reports no changes
- flake8 reports no warnings
- documentation is updated when behavior changes
- the pull request explains what changed, why, and how it was tested

GitHub Actions repeats the checks on Python 3.12, 3.13, and 3.14.

## Release process

For maintainers:

1. Update the version in `pyproject.toml` and `gmshparser/__init__.py`.
2. Update the changelog.
3. Build locally with `uv build --no-sources`.
4. Create and publish the GitHub release.
5. The release workflow builds, smoke-tests, and publishes the distributions with `uv`.

A manual publication can be performed with:

```bash
uv build --no-sources
uv publish
```

## License

By contributing, you agree that your contribution is licensed under the MIT License.
