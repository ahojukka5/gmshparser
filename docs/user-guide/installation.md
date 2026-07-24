# Installation

## Install from PyPI

Install the latest stable release with `uv`:

```bash
uv add gmshparser
```

The package can also be installed with pip:

```bash
pip install gmshparser
```

## Install the development version

Install directly from GitHub:

```bash
uv add git+https://github.com/ahojukka5/gmshparser.git
```

or with pip:

```bash
pip install git+https://github.com/ahojukka5/gmshparser.git
```

## Visualization dependencies

The parser itself does not depend on matplotlib. Install it separately when using the visualization examples:

```bash
uv add matplotlib
```

For a repository checkout, the predefined dependency group can be used instead:

```bash
uv sync --group visualization
```

## Verify the installation

```bash
uv run python -c "import gmshparser; print(gmshparser.__version__)"
```

## Development installation

Clone the repository and let `uv` create the environment:

```bash
git clone https://github.com/ahojukka5/gmshparser.git
cd gmshparser
uv sync
```

The default development environment contains the `test` and `lint` groups. Other groups are installed explicitly:

```bash
# Documentation toolchain
uv sync --group docs

# Visualization examples
uv sync --group visualization

# Every development group
uv sync --all-groups
```

Run commands through the managed environment:

```bash
uv run pytest
uv run black . --check
uv run flake8 gmshparser tests
```

Dependency lock files are intentionally not committed in this repository. `uv` may create a local `uv.lock`; it is ignored by Git.

## System requirements

- Python 3.12 or later
- A current version of `uv`, recommended for development

## Troubleshooting

Check the interpreter selected by `uv`:

```bash
uv run python --version
```

Recreate the environment when dependency state becomes inconsistent:

```bash
rm -rf .venv uv.lock
uv sync
```

## Upgrading

```bash
uv add --upgrade gmshparser
```

With pip:

```bash
pip install --upgrade gmshparser
```

## Uninstalling

```bash
uv remove gmshparser
```

With pip:

```bash
pip uninstall gmshparser
```
