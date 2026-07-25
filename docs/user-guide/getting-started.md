# Getting Started

gmshparser reads supported **ASCII** Gmsh `.msh` files. New code should use the immutable modern model returned by `gmshparser.read()`.

## Requirements

- Python 3.12 or newer
- no runtime dependencies for core parsing
- a supported ASCII MSH file: 1.0, 2.0–2.2, or 4.0–4.1

## Install

```bash
uv add gmshparser
```

or:

```bash
pip install gmshparser
```

## Read a mesh

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")

print(f"file: {mesh.name}")
print(f"MSH version: {mesh.version}")
print(f"nodes: {len(mesh.nodes)}")
print(f"elements: {len(mesh.elements)}")
print(f"dimension: {mesh.dimension}")
```

The format version is detected automatically. Unsupported versions, binary files, malformed sections, and invalid connectivity raise structured parser errors.

## Inspect nodes

```python
for node in mesh.nodes:
    print(node.tag, node.coordinates)
```

Look up a node by its original Gmsh tag:

```python
node = mesh.nodes[42]
print(node.x, node.y, node.z)
```

## Inspect elements

```python
from gmshparser import ElementType

for element in mesh.elements:
    print(element.tag, element.element_type, element.node_tags)

triangles = mesh.elements.by_type(ElementType.TRIANGLE)
```

Modern elements reference their `Node` objects directly:

```python
for triangle in triangles:
    coordinates = [node.coordinates for node in triangle]
```

## Inspect entities

```python
surface = mesh.entity(dimension=2, tag=7)
print(surface.nodes)
print(surface.elements)
```

The complete entity collection can also be filtered:

```python
surfaces = mesh.entities.by_dimension(2)
```

## Physical groups

```python
walls = mesh.physical_groups["Walls"]
print(walls.elements)
print(walls.nodes)
```

Use `(dimension, tag)` for anonymous or ambiguously named groups.

## Read generated text

```python
from io import StringIO

mesh = gmshparser.read(StringIO(msh_text), name="generated.msh")
```

The supplied name is used in diagnostics.

## Handle errors

```python
try:
    mesh = gmshparser.read("mesh.msh")
except gmshparser.ParseError as error:
    print(error)
    print(error.filename, error.line_number, error.section)
```

## Existing applications

The original mutable API remains available:

```python
legacy_mesh = gmshparser.parse("mesh.msh")
print(legacy_mesh.get_number_of_nodes())
```

Top-level `parse()` intentionally keeps its historical return type.

## Continue

- [Modern Data Model](pythonic-api.md)
- [Working with Meshes](basic-usage.md)
- [Physical Groups and Periodicity](physical-groups.md)
- [Error Handling](error-handling.md)
- [Supported Formats](supported-formats.md)
- [API Reference](../api/overview.md)
