# Installation

## Install from PyPI (Recommended)

The easiest way to install gmshparser is from the Python Package Index (PyPI):

```bash
pip install gmshparser
```

This will install the latest stable release.

## Install from GitHub (Development Version)

To install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/ahojukka5/gmshparser.git
```

## Install with Poetry

If you're using Poetry for dependency management:

```bash
poetry add gmshparser
```

## Install with Optional Dependencies

If you want visualization support with matplotlib:

```bash
pip install gmshparser matplotlib
```

## Verify Installation

After installation, verify that gmshparser is working correctly:

```python
import gmshparser
print(gmshparser.__version__)
```

Or test the command-line interface:

```bash
gmshparser --help
```

## Development Installation

If you want to contribute to gmshparser, clone the repository and install in development mode:

```bash
# Clone the repository
git clone https://github.com/ahojukka5/gmshparser.git
cd gmshparser

# Install with Poetry (recommended)
poetry install

# Or install with pip in editable mode
pip install -e .
```

## System Requirements

### Minimum Requirements

- Python 3.8.1 or later
- pip or Poetry

### Recommended Setup

- Python 3.10 or later
- Virtual environment (venv, conda, or Poetry)

### Optional Dependencies

- **matplotlib** (>=3.5, <3.11): For mesh visualization
- **mkdocs** (>=1.6): For building documentation (development only)

## Troubleshooting

### Python Version Issues

If you see errors about Python version, ensure you're using Python 3.8.1 or later:

```bash
python --version
```

### Permission Errors

If you encounter permission errors during installation, try:

```bash
pip install --user gmshparser
```

Or use a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install gmshparser
```

### Import Errors

If you can install but can't import the package, check that you're using the correct Python environment:

```bash
which python
which pip
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade gmshparser
```

## Uninstalling

To remove gmshparser:

```bash
pip uninstall gmshparser
```
