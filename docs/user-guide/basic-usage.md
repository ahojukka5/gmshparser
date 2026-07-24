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
print(mesh.version.major, mesh.version.minor)
print(mesh.is_ascii)
print(mesh.data_size)
print(mesh.dimension)
print(mesh.bounds)
print(len(mesh.nodes), len(mesh.elements), len(mesh.entities))
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
selected_entity = mesh.nodes.where(entity=(2, 7))
parametric_nodes = mesh.nodes.where(parametric=True)
```

## Elements

Elements carry direct references to their nodes:

```python
for element in mesh.elements:
    print(element.tag, element.type, element.node_tags)
    for node in element:
        print(node.coordinates)
```

Index and filter using collection operations:

```python
from gmshparser.api import ElementType

element = mesh.elements[17]
triangles = mesh.elements.by_type(ElementType.TRIANGLE)
quads = mesh.elements.where(
    element_type=ElementType.QUADRANGLE,
    dimension=2,
)
```

`ElementType` is an integer enum. It gives common Gmsh IDs readable names while
remaining comparable with the corresponding integer values.

## Entities

Most code can use the flat collections. Unified entities retain the original
Gmsh grouping when it matters:

```python
for entity in mesh.entities:
    print(entity.dimension, entity.tag, entity.element_types)
    print(len(entity.nodes), len(entity.elements))
```

Look up an entity using `(dimension, tag)`:

```python
surface = mesh.entities[(2, 7)]
```

Filter entities by dimension, content, or element type:

```python
surfaces = mesh.entities.where(dimension=2)
triangle_entities = mesh.entities.where(element_type=ElementType.TRIANGLE)
entities_with_elements = mesh.entities.where(has_elements=True)
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
