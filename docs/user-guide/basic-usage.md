# Basic Usage

## Read a mesh

```python
import gmshparser

mesh = gmshparser.read("path/to/mesh.msh")
```

`read()` detects the supported MSH version automatically and returns the modern,
immutable `gmshparser.api.Mesh` model.

## Mesh metadata

```python
print(mesh.name)
print(mesh.version)
print(mesh.version_info)
print(mesh.is_ascii)
print(mesh.precision)
print(mesh.bounds)
print(len(mesh.nodes), len(mesh.elements))
```

## Nodes

The flat node collection iterates over node objects:

```python
for node in mesh.nodes:
    print(node.tag, node.coordinates)
    print(node.x, node.y, node.z)
```

Index by the original Gmsh tag:

```python
node = mesh.nodes[42]
x, y, z = node
```

Filter by entity metadata:

```python
surface_nodes = mesh.nodes.where(dimension=2)
selected_entity = mesh.nodes.where(dimension=2, entity_tag=7)
```

## Elements

```python
for element in mesh.elements:
    print(
        element.tag,
        element.element_type,
        element.node_tags,
        element.dimension,
        element.entity_tag,
    )
```

Index and filter using collection operations:

```python
element = mesh.elements[17]
triangles = mesh.elements.by_type(2)
quads = mesh.elements.where(element_type=3, dimension=2)
```

Gmsh element types are numeric. Common values include 1 for a two-node line, 2
for a three-node triangle, 3 for a four-node quadrangle, and 4 for a four-node
tetrahedron.

## Entity blocks

Most code can use the flat collections. Entity blocks remain available when the
original Gmsh grouping matters:

```python
for entity in mesh.element_entities:
    print(entity.dimension, entity.tag, entity.element_type)
    for element in entity:
        print(element.tag)
```

Look up an entity using `(dimension, tag)`:

```python
surface = mesh.element_entities[(2, 7)]
```

## Visualization helpers

The helpers accept modern meshes directly:

```python
X, Y, triangles = gmshparser.helpers.get_triangles(mesh)
X, Y, quads = gmshparser.helpers.get_quads(mesh)
mixed = gmshparser.helpers.get_elements_2d(mesh)
```

`get_triangles()` and `get_quads()` return zero-based connectivity into their
coordinate arrays. `get_elements_2d()` preserves original node tags in element
connectivity.

## Export nodes to CSV

```python
import csv

with open("nodes.csv", "w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["id", "x", "y", "z"])
    writer.writerows((node.tag, *node.coordinates) for node in mesh.nodes)
```

## Read from an open stream

```python
from io import StringIO

mesh = gmshparser.read(StringIO(msh_text), name="generated.msh")
```

## Error handling

```python
try:
    mesh = gmshparser.read("mesh.msh")
except FileNotFoundError:
    print("Mesh file not found")
except ValueError as error:
    print(f"Unsupported or invalid MSH file: {error}")
```

## Compatibility API

The original parser-oriented model remains available:

```python
legacy_mesh = gmshparser.parse("mesh.msh")

for entity in legacy_mesh.get_node_entities():
    for node in entity.get_nodes():
        print(node.get_tag(), node.get_coordinates())
```

See [Pythonic API](pythonic-api.md) for the complete modern model and migration
notes.
