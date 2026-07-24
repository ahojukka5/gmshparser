# Installation

## Stable release

Add gmshparser to a uv-managed project:

```bash
uv add gmshparser
```

Install it into the active Python environment with pip:

```bash
pip install gmshparser
```

The package requires Python 3.12 or newer.

## Development version

Install the current `master` branch directly from GitHub:

```bash
uv add "gmshparser @ git+https://github.com/ahojukka5/gmshparser.git"
```

or with pip:

```bash
pip install git+https://github.com/ahojukka5/gmshparser.git
```

## Verify the installation

```bash
python -c "import gmshparser; print(gmshparser.__version__)"
gmshparser --version
```

In a uv-managed project, prefix commands with `uv run` when needed:

```bash
uv run python -c "import gmshparser; print(gmshparser.__version__)"
uv run gmshparser --version
```

## Visualization dependency

The core package does not depend on matplotlib. Add it only for visualization:

```bash
uv add matplotlib
```

For a repository checkout, use the predefined dependency group:

```bash
uv sync --group visualization
```

## Development environment

Clone the repository and let uv create the local environment:

```bash
git clone https://github.com/ahojukka5/gmshparser.git
cd gmshparser
uv sync
```

The default `dev` group includes the `test` and `lint` groups. Install other
groups explicitly:

```bash
uv sync --group docs
uv sync --group visualization
uv sync --all-groups
```

Run project commands through uv:

```bash
uv run pytest
uv run ruff format --check gmshparser tests examples
uv run ruff check gmshparser tests examples
```

Dependency lock files are intentionally not committed. A locally generated
`uv.lock` is ignored by Git.

## Upgrade

In a uv project:

```bash
uv add gmshparser --upgrade-package gmshparser
```

With pip:

```bash
pip install --upgrade gmshparser
```

## Uninstall

Remove the dependency from a uv project:

```bash
uv remove gmshparser
```

With pip:

```bash
pip uninstall gmshparser
```
