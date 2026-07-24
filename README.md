# gmshparser — parse Gmsh `.msh` files

[![Python CI][gh-ci-img]][gh-ci-url]
[![codecov][codecov-img]][codecov-url]
[![PyPI - Version][pypi-img]][pypi-url]
[![PyPI - Downloads][pypi-dl-img]][pypi-dl-url]
[![Documentation][docs-img]][docs-url]
[![Python Version][python-img]][pypi-url]
[![License][license-img]][license-url]

![gmshparser hero image](docs/hero-image.webp)

gmshparser is a small, dependency-free Python package for reading **ASCII**
[Gmsh](https://gmsh.info/) MSH files. It provides a consistent object model for
nodes, elements, and entities across the supported format versions.

- **Python:** 3.12 or newer
- **MSH formats:** 1.0, 2.0, 2.1, 2.2, 4.0, and 4.1
- **Core dependencies:** none
- **Scope:** reading meshes; writing and binary MSH files are not supported

Project links:

- [Documentation](https://ahojukka5.github.io/gmshparser/)
- [PyPI package](https://pypi.org/project/gmshparser)
- [Issue tracker](https://github.com/ahojukka5/gmshparser/issues)

## Installation

Install the stable release with uv:

```bash
uv add gmshparser
```

or with pip:

```bash
pip install gmshparser
```

Install the current development version directly from GitHub:

```bash
uv add "gmshparser @ git+https://github.com/ahojukka5/gmshparser.git"
```

## Python API

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")
print(mesh)
```

Iterate over nodes:

```python
for entity in mesh.get_node_entities():
    for node in entity.get_nodes():
        print(node.get_tag(), node.get_coordinates())
```

Iterate over elements:

```python
for entity in mesh.get_element_entities():
    element_type = entity.get_element_type()
    for element in entity.get_elements():
        print(element.get_tag(), element_type, element.get_connectivity())
```

The parser detects the MSH version automatically. See the
[Basic Usage guide](https://ahojukka5.github.io/gmshparser/user-guide/basic-usage/)
for the complete data-access examples.

## Command-line interface

The installed `gmshparser` command can print a mesh summary, nodes, or elements:

```bash
gmshparser mesh.msh info
gmshparser mesh.msh nodes
gmshparser mesh.msh elements
gmshparser --version
```

`nodes` output begins with the node count, followed by
`node_id x y z`. `elements` output begins with the element count, followed by
`element_id element_type connectivity...`.

## Visualization helpers

Matplotlib is optional. The triangle helper returns zero-based connectivity
suitable for `matplotlib.triplot`:

```python
import gmshparser
import matplotlib.pyplot as plt

mesh = gmshparser.parse("mesh.msh")
X, Y, triangles = gmshparser.helpers.get_triangles(mesh)
plt.triplot(X, Y, triangles)
plt.axis("equal")
plt.show()
```

Install the optional dependency separately:

```bash
uv add matplotlib
```

## Development

The repository uses uv and intentionally does not commit dependency lock files.
Ruff provides both formatting and linting.

```bash
git clone https://github.com/ahojukka5/gmshparser.git
cd gmshparser
uv sync
uv run ruff format --check gmshparser tests examples
uv run ruff check gmshparser tests examples
uv run pytest
```

Build the documentation with:

```bash
uv sync --group docs
uv run mkdocs build
```

See the [Contributing guide](https://ahojukka5.github.io/gmshparser/developer-guide/contributing/)
for dependency groups and the release workflow.

## License

gmshparser is released under the MIT License.

[gh-ci-img]: https://github.com/ahojukka5/gmshparser/actions/workflows/python.yml/badge.svg
[gh-ci-url]: https://github.com/ahojukka5/gmshparser/actions/workflows/python.yml
[codecov-img]: https://codecov.io/gh/ahojukka5/gmshparser/branch/master/graph/badge.svg
[codecov-url]: https://codecov.io/gh/ahojukka5/gmshparser
[pypi-img]: https://img.shields.io/pypi/v/gmshparser
[pypi-url]: https://pypi.org/project/gmshparser
[pypi-dl-img]: https://img.shields.io/pypi/dm/gmshparser
[pypi-dl-url]: https://pypi.org/project/gmshparser
[docs-img]: https://img.shields.io/badge/docs-GitHub%20Pages-blue
[docs-url]: https://ahojukka5.github.io/gmshparser/
[python-img]: https://img.shields.io/pypi/pyversions/gmshparser
[license-img]: https://img.shields.io/github/license/ahojukka5/gmshparser
[license-url]: https://github.com/ahojukka5/gmshparser/blob/master/LICENSE
