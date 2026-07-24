# Pythonic API

`gmshparser.read()` is the recommended entry point for new code. It returns an
immutable mesh model designed around normal Python attributes, iteration, tag
lookup, and small filtering operations.

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")
```

The original `gmshparser.parse()` API remains available for compatibility.

## Mesh metadata

Metadata is exposed as attributes rather than `get_*` methods:

```python
print(mesh.name)
print(mesh.version)       # 4.1
print(mesh.version_info)  # (4, 1)
print(mesh.is_ascii)
print(mesh.precision)
print(mesh.bounds)        # ((xmin, ymin, zmin), (xmax, ymax, zmax))
```

Counts follow normal Python collection conventions:

```python
print(len(mesh.nodes))
print(len(mesh.elements))
print(len(mesh.node_entities))
print(len(mesh.element_entities))
```

## Nodes

`mesh.nodes` iterates over node objects and uses Gmsh tags for indexing:

```python
for node in mesh.nodes:
    print(node.tag, node.x, node.y, node.z)

node = mesh.nodes[42]
print(node.coordinates)
```

A node can also be unpacked as coordinates:

```python
x, y, z = mesh.nodes[42]
```

Useful collection operations include:

```python
print(mesh.nodes.tags)
node = mesh.nodes.get(42)
surface_nodes = mesh.nodes.where(dimension=2)
entity_nodes = mesh.nodes.where(dimension=2, entity_tag=7)
coordinates = mesh.nodes.coordinates
```

Iteration deliberately yields node objects rather than dictionary keys. Integer
indexing always means a Gmsh tag, not a positional index.

## Elements

Elements are similarly flat and tag-addressable:

```python
for element in mesh.elements:
    print(
        element.tag,
        element.element_type,
        element.node_tags,
        element.dimension,
        element.entity_tag,
    )

quad = mesh.elements[12]
print(quad.connectivity)
```

`element.type` is a concise alias for `element.element_type`, and iterating an
element yields its node tags.

Filter without manually traversing entity blocks:

```python
triangles = mesh.elements.by_type(2)
surface_quads = mesh.elements.where(element_type=3, dimension=2)
entity_elements = mesh.elements.where(dimension=2, entity_tag=7)
print(mesh.elements.types)
```

The returned filtered collections support the same iteration, tag lookup, and
collection operations as `mesh.elements`.

## Entity-level access

Entity information is still available when it matters. Entity collections are
indexed by `(dimension, tag)`:

```python
surface = mesh.node_entities[(2, 7)]
for node in surface:
    print(node.tag)

cell_block = mesh.element_entities[(3, 1)]
print(cell_block.element_type)
for element in cell_block:
    print(element.tag)
```

Filter entities by dimension:

```python
surfaces = mesh.element_entities.where(dimension=2)
```

## Read from a text stream

`read()` accepts open text streams in addition to paths:

```python
from io import StringIO

mesh = gmshparser.read(StringIO(msh_text), name="generated.msh")
```

This is useful for generated meshes and tests without temporary files.

## Visualization helpers

The existing helpers accept the modern model:

```python
X, Y, triangles = gmshparser.helpers.get_triangles(mesh)
X, Y, quads = gmshparser.helpers.get_quads(mesh)
mixed = gmshparser.helpers.get_elements_2d(mesh)
```

## Compatibility API

Existing applications can continue unchanged:

```python
legacy_mesh = gmshparser.parse("mesh.msh")

for entity in legacy_mesh.get_node_entities():
    for node in entity.get_nodes():
        print(node.get_tag(), node.get_coordinates())
```

`parse()` and the mutable parser-oriented classes are retained. New applications
should prefer `read()` and the classes in `gmshparser.api`.
