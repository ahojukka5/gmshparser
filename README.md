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
[Gmsh](https://gmsh.info/) MSH files. It provides a modern immutable API for
normal application code while retaining the original parser-oriented API for
backward compatibility.

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

## Entry points

The original top-level entry point is intentionally unchanged:

| Call | Result |
| --- | --- |
| `gmshparser.parse(path)` | original mutable compatibility `Mesh` |
| `gmshparser.read(path)` | modern immutable `ModernMesh` |
| `gmshparser.api.parse(path)` | modern immutable `Mesh` in the explicit modern namespace |

This means existing applications using `gmshparser.parse()` continue to behave
exactly as before.

## Pythonic API

Use `read()` for ordinary new code:

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")
print(mesh.version, len(mesh.nodes), len(mesh.elements))
```

Applications that prefer the verb `parse` can opt into the modern namespace:

```python
from gmshparser.api import parse

mesh = parse("mesh.msh")
```

Collections iterate over value objects and use original Gmsh tags for lookup:

```python
for node in mesh.nodes:
    print(node.tag, node.x, node.y, node.z)

node = mesh.nodes[42]
element = mesh.elements[17]
```

Elements link directly to their nodes and expose a typed element kind:

```python
from gmshparser import ElementType

triangles = mesh.elements.by_type(ElementType.TRIANGLE)

for triangle in triangles:
    print(triangle.tag, triangle.element_type, triangle.node_tags)
    for node in triangle:
        print(node.coordinates)
```

Entity context is available without separate node and element block APIs:

```python
surface = mesh.entity(dimension=2, tag=7)
print(len(surface.nodes), len(surface.elements), surface.element_types)

print(mesh.surfaces)
print(mesh.volumes)
```

### Physical groups

Named and anonymous physical groups are available directly from the modern
model. Names from `$PhysicalNames` and assignments from MSH 1.x, 2.x, and 4.x
are retained:

```python
walls = mesh.physical_groups["Walls"]
domain = mesh.physical_groups[(3, 2)]

for element in walls.elements:
    print(element.tag, element.physical_tags)

print(walls.entities)
print(walls.nodes)
```

A convenience method also accepts a name or a numeric tag:

```python
walls = mesh.physical_group("Walls")
domain = mesh.physical_group(2, dimension=3)
```

`read()` accepts filesystem paths, `Path` objects, and open text streams. See the
[Pythonic API guide](https://ahojukka5.github.io/gmshparser/user-guide/pythonic-api/)
for the complete model.

## Periodic meshes

Periodic entity relations from MSH 2.x and 4.x are available through the modern
model:

```python
link = mesh.periodic_links[(2, 7)]
print(link.master_entity_tag, link.affine_transform)
for slave_node_tag, master_node_tag in link.node_pairs:
    print(slave_node_tag, master_node_tag)
```

The compatibility model exposes the same records through
`get_periodic_link()` and `get_periodic_links()`.

## NumPy interoperability

NumPy support is optional:

```bash
uv add "gmshparser[numpy]"
```

Convert the modern mesh into detached array data:

```python
import gmshparser.numpy as gnp
from gmshparser import ElementType

arrays = gnp.to_numpy(mesh)
triangles = arrays.cells[ElementType.TRIANGLE]
triangle_points = arrays.points[triangles.connectivity]
triangle_node_tags = arrays.cell_node_tags(ElementType.TRIANGLE)
```

Cell connectivity contains zero-based rows into `arrays.points`. Original Gmsh
node tags, element tags, and entity keys remain available alongside the arrays.
Mixed meshes are represented as rectangular cell blocks grouped by element type.

## Structured parser errors

Both entry points expose the same error hierarchy and source context:

```python
try:
    mesh = gmshparser.read("broken.msh")
except gmshparser.ParseError as error:
    print(error)
    print(error.filename)
    print(error.line_number)
    print(error.section)
    print(error.line)
```

A typical message is:

```text
broken.msh:127 [$Elements]: Element 42 requires 3 nodes, got 4
```

Specific errors include `UnsupportedVersionError`,
`UnsupportedBinaryFormatError`, `UnexpectedEndOfFileError`,
`InvalidNodeError`, `InvalidElementError`, and
`InvalidElementConnectivityError`. Every `ParseError` is also a `ValueError`, so
existing broad handlers continue to work. The parser does not print failures to
stdout or stderr.

See the [error-handling guide](https://ahojukka5.github.io/gmshparser/user-guide/error-handling/)
for the full hierarchy and recovery examples.

## Compatibility API

Existing applications using the original mutable `get_*` / `set_*` model can
continue unchanged:

```python
legacy_mesh = gmshparser.parse("mesh.msh")

for entity in legacy_mesh.get_node_entities():
    for node in entity.get_nodes():
        print(node.get_tag(), node.get_coordinates())
```

The parser detects the MSH version automatically in both APIs.

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

Matplotlib is optional. Helpers accept both the modern and compatibility mesh
models:

```python
import gmshparser
import matplotlib.pyplot as plt

mesh = gmshparser.read("mesh.msh")
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
