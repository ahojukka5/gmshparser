from pathlib import Path


def replace(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text()
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old!r}")
    target.write_text(text.replace(old, new, 1))


replace(
    "README.md",
    """- **Core dependencies:** none
- **Scope:** reading meshes; writing and binary MSH files are not supported
""",
    """- **Core dependencies:** none
- **Typing:** PEP 561 inline type information through `py.typed`
- **Scope:** reading meshes; writing and binary MSH files are not supported
""",
)
replace(
    "README.md",
    """The repository uses uv and intentionally does not commit dependency lock files.
Ruff provides both formatting and linting.
""",
    """The repository uses uv and intentionally does not commit dependency lock files.
Ruff provides formatting and linting, while mypy validates both the package and a
strict downstream public-API example.
""",
)
replace(
    "README.md",
    """uv run ruff format --check gmshparser tests examples
uv run ruff check gmshparser tests examples
uv run pytest
""",
    """uv run ruff format --check gmshparser tests examples benchmarks
uv run ruff check gmshparser tests examples benchmarks
uv run mypy gmshparser
uv run mypy --strict tests/typing/public_api.py
uv run pytest
""",
)
replace(
    "README.md",
    "uv run mkdocs build\n",
    "uv run mkdocs build --strict\n",
)

replace(
    "docs/user-guide/installation.md",
    """The package requires Python 3.12 or newer.

## Development version
""",
    """The package requires Python 3.12 or newer.

## Typing support

gmshparser ships inline PEP 561 type information and a `py.typed` marker. Type
checkers such as mypy and pyright therefore use the annotations from the installed
package without a separate stubs distribution.

## Development version
""",
)
replace(
    "docs/user-guide/installation.md",
    """The default `dev` group includes the `test` and `lint` groups. Install other
groups explicitly:
""",
    """The default `dev` group includes the `test`, `lint`, and `typing` groups.
Install other groups explicitly:
""",
)
replace(
    "docs/user-guide/installation.md",
    """uv sync --group docs
uv sync --group visualization
uv sync --all-groups
""",
    """uv sync --group docs
uv sync --group benchmark
uv sync --group visualization
uv sync --all-groups
""",
)
replace(
    "docs/user-guide/installation.md",
    """uv run pytest
uv run ruff format --check gmshparser tests examples
uv run ruff check gmshparser tests examples
""",
    """uv run pytest
uv run ruff format --check gmshparser tests examples benchmarks
uv run ruff check gmshparser tests examples benchmarks
uv run mypy gmshparser
uv run mypy --strict tests/typing/public_api.py
""",
)

replace(
    "docs/developer-guide/contributing.md",
    """uv sync --group docs
uv sync --group benchmark
uv sync --group visualization
""",
    """uv sync --group docs
uv sync --group benchmark
uv sync --group typing
uv sync --group visualization
""",
)
replace(
    "docs/developer-guide/contributing.md",
    """uv run ruff format --check gmshparser tests examples benchmarks
uv run ruff check gmshparser tests examples benchmarks
uv run pytest
""",
    """uv run ruff format --check gmshparser tests examples benchmarks
uv run ruff check gmshparser tests examples benchmarks
uv run mypy gmshparser
uv run mypy --strict tests/typing/public_api.py
uv run pytest
uv run mkdocs build --strict
""",
)
replace(
    "docs/developer-guide/contributing.md",
    """| `lint` | Ruff formatting and linting |
| `docs` | MkDocs documentation toolchain |
""",
    """| `lint` | Ruff formatting and linting |
| `typing` | mypy and dependencies used by typing checks |
| `docs` | MkDocs documentation toolchain |
""",
)
replace(
    "docs/developer-guide/contributing.md",
    """uv add --group lint PACKAGE
uv add --group docs PACKAGE
""",
    """uv add --group lint PACKAGE
uv add --group typing PACKAGE
uv add --group docs PACKAGE
""",
)
replace(
    "docs/developer-guide/contributing.md",
    """- Add type hints where they improve clarity.
- Write tests for new behavior and bug fixes.
""",
    """- Keep package and downstream public-API mypy checks clean.
- Add precise type hints without hiding errors behind broad ignores.
- Write tests for new behavior and bug fixes.
""",
)
replace(
    "docs/developer-guide/contributing.md",
    "uv run mkdocs build\n",
    "uv run mkdocs build --strict\n",
)
replace(
    "docs/developer-guide/contributing.md",
    """- `quality` runs Ruff once on Python 3.12
- `test` runs pytest on Python 3.12, 3.13, and 3.14
""",
    """- `quality` runs Ruff once on Python 3.12
- `typing` runs mypy on package sources and a strict downstream API example
- `test` runs pytest on Python 3.12, 3.13, and 3.14
""",
)
replace(
    "docs/developer-guide/contributing.md",
    """- `ruff check` reports no violations
- documentation is updated when behavior changes
""",
    """- `ruff check` reports no violations
- package and downstream typing checks pass
- strict documentation build reports no warnings
- documentation is updated when behavior changes
""",
)
replace(
    "docs/developer-guide/contributing.md",
    """3. Build locally with `uv build --no-sources`.
4. Create and publish a GitHub release tagged `v<project-version>`.
""",
    """3. Run the complete quality, typing, test, strict documentation, and package
   checks.
4. Build locally with `uv build --no-sources` and verify that `py.typed` is present
   in both distributions.
5. Create and publish a GitHub release tagged `v<project-version>`.
""",
)
replace(
    "docs/developer-guide/contributing.md",
    """5. The release workflow verifies that the tag matches the project version.
6. The workflow builds and smoke-tests both distributions.
7. `uv publish` obtains a short-lived PyPI credential through GitHub OIDC.
""",
    """6. The release workflow verifies that the tag matches the project version.
7. The workflow builds and smoke-tests both distributions.
8. `uv publish` obtains a short-lived PyPI credential through GitHub OIDC.
""",
)

replace(
    "docs/developer-guide/test-results.md",
    """The test matrix runs on Python 3.12, 3.13, and 3.14:
""",
    """The typing job validates package sources and a strict downstream public-API
sample:

```bash
uv sync --no-default-groups --group typing
uv run --no-sync mypy gmshparser
uv run --no-sync mypy --strict tests/typing/public_api.py
```

The test matrix runs on Python 3.12, 3.13, and 3.14:
""",
)
replace(
    "docs/developer-guide/test-results.md",
    """After quality and tests succeed, a separate package job builds the wheel and
source distribution and smoke-tests the installed package and CLI.
""",
    """After quality, typing, and tests succeed, a separate package job builds the
wheel and source distribution and smoke-tests the installed package, CLI, and
packaged `py.typed` marker.
""",
)
replace(
    "docs/developer-guide/test-results.md",
    "uv run --no-sync mkdocs build\n",
    "uv run --no-sync mkdocs build --strict\n",
)

replace(
    "docs/developer-guide/testing.md",
    """The repository uses pytest, pytest-cov, and Ruff through uv dependency groups.
Ruff handles both formatting and linting.
""",
    """The repository uses pytest, pytest-cov, Ruff, and mypy through uv dependency
groups. Ruff handles formatting and linting; mypy validates inline package types
and downstream API use.
""",
)
replace(
    "docs/developer-guide/testing.md",
    "The default `dev` group includes the `test` and `lint` groups.\n",
    "The default `dev` group includes the `test`, `lint`, and `typing` groups.\n",
)
replace(
    "docs/developer-guide/testing.md",
    """uv run ruff format --check gmshparser tests examples
uv run ruff check gmshparser tests examples
""",
    """uv run ruff format --check gmshparser tests examples benchmarks
uv run ruff check gmshparser tests examples benchmarks
""",
)
replace(
    "docs/developer-guide/testing.md",
    """uv run ruff check --fix gmshparser tests examples
uv run ruff format gmshparser tests examples
""",
    """uv run ruff check --fix gmshparser tests examples benchmarks
uv run ruff format gmshparser tests examples benchmarks
""",
)
replace(
    "docs/developer-guide/testing.md",
    """Run the coverage command used by the CI test job:
""",
    """## Static typing

Run the same package and downstream checks as CI:

```bash
uv run mypy gmshparser
uv run mypy --strict tests/typing/public_api.py
```

The packaged `py.typed` marker is tested from both built distribution formats.

Run the coverage command used by the CI test job:
""",
)
replace(
    "docs/developer-guide/testing.md",
    """GitHub Actions runs Ruff once in a dedicated quality job, pytest on Python 3.12,
3.13, and 3.14, and distribution builds plus package smoke tests after those jobs
succeed. The documentation workflow builds MkDocs separately and deploys only on
pushes to `master`.
""",
    """GitHub Actions runs Ruff in a quality job, mypy in a typing job, and pytest on
Python 3.12, 3.13, and 3.14. Distribution builds and package smoke tests run only
after those jobs succeed. The documentation workflow performs a strict MkDocs
build and deploys only on pushes to `master`.
""",
)
