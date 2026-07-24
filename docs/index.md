# gmshparser

[![Python CI][gh-ci-img]][gh-ci-url]
[![codecov][codecov-img]][codecov-url]
[![PyPI - Version][pypi-img]][pypi-url]
[![PyPI - Downloads][pypi-dl-img]][pypi-dl-url]
[![Documentation][documentation-img]][documentation-url]

**A lightweight, dependency-free Python package for parsing ASCII Gmsh MSH files.**

gmshparser reads supported [Gmsh](https://gmsh.info/) mesh formats into a
consistent Python object model. The package focuses on parsing and inspection;
it does not write meshes or support binary MSH files.

## Key features

- MSH 1.0, 2.0, 2.1, 2.2, 4.0, and 4.1 support
- automatic format-version detection
- no runtime dependencies
- Python 3.12 or newer
- Python API and command-line interface
- optional matplotlib helpers for 2D meshes

## Quick start

Install the package:

```bash
uv add gmshparser
```

or:

```bash
pip install gmshparser
```

Parse a mesh:

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")
print(
    f"Loaded {mesh.get_number_of_nodes()} nodes and "
    f"{mesh.get_number_of_elements()} elements"
)
```

## Supported formats

| Version | File structure | Status |
| --- | --- | --- |
| MSH 1.0 | legacy `$NOD` and `$ELM` sections | supported, ASCII |
| MSH 2.0–2.2 | `$MeshFormat`, `$Nodes`, and `$Elements` | supported, ASCII |
| MSH 4.0–4.1 | entity-block node and element sections | supported, ASCII |

See [Supported Formats](user-guide/supported-formats.md) for limitations and
format-specific notes.

## Documentation

- [Getting Started](user-guide/getting-started.md)
- [Basic Usage](user-guide/basic-usage.md)
- [Command-line Interface](user-guide/cli.md)
- [Visualization](user-guide/visualization.md)
- [Contributing](developer-guide/contributing.md)
- [API Reference](api/overview.md)

## Project links

- [Source repository](https://github.com/ahojukka5/gmshparser)
- [Issue tracker](https://github.com/ahojukka5/gmshparser/issues)
- [PyPI package](https://pypi.org/project/gmshparser)
- [MIT License](about/license.md)

[gh-ci-img]: https://github.com/ahojukka5/gmshparser/actions/workflows/python.yml/badge.svg
[gh-ci-url]: https://github.com/ahojukka5/gmshparser/actions/workflows/python.yml
[codecov-img]: https://codecov.io/gh/ahojukka5/gmshparser/branch/master/graph/badge.svg
[codecov-url]: https://codecov.io/gh/ahojukka5/gmshparser
[pypi-img]: https://img.shields.io/pypi/v/gmshparser
[pypi-url]: https://pypi.org/project/gmshparser
[pypi-dl-img]: https://img.shields.io/pypi/dm/gmshparser
[pypi-dl-url]: https://pypi.org/project/gmshparser
[documentation-img]: https://img.shields.io/badge/docs-GitHub%20Pages-blue
[documentation-url]: https://ahojukka5.github.io/gmshparser/
