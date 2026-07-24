# Pythonic API

`gmshparser.read()` is the recommended entry point for new code. It returns an
immutable model built around normal Python attributes, iteration, tag lookup,
direct object relationships, and small filtering operations.

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")
```

The original `gmshparser.parse()` API remains available for compatibility.

## Mesh metadata

```python
print(mesh.name)
print(mesh.version)        # 4.1
print(mesh.version.major)  # 4
print(mesh.version.minor)  # 1
print(mesh.is_ascii)
print(mesh.data_size)      # 8 bytes in the MSH header
print(mesh.dimension)
print(mesh.bounds)         # ((xmin, ymin, zmin), (xmax, ymax, zmax))
```

Counts follow normal collection conventions:

```python
print(len(mesh.nodes))
print(len(mesh.elements))
print(len(mesh.entities))
```

## Nodes

`mesh.nodes` iterates over node objects and uses original Gmsh tags for lookup:

```python
for node in mesh.nodes:
    print(node.tag, node.x, node.y, node.z)

node = mesh.nodes[42]
print(node.coordinates)
```

A node can be unpacked as Cartesian coordinates:

```python
x, y, z = mesh.nodes[42]
```

Useful collection operations include:

```python
print(mesh.nodes.tags)
node = mesh.nodes.get(42)
surface_nodes = mesh.nodes.where(dimension=2)
entity_nodes = mesh.nodes.where(entity=(2, 7))
coordinates = mesh.nodes.coordinates
```

Parametric MSH node coordinates are kept separately instead of being mixed into
the Cartesian tuple:

```python
print(node.parametric_coordinates)
print(node.is_parametric)
```

Integer indexing always means a Gmsh tag, not a positional index.

## Elements

Elements are flat and tag-addressable. They reference `Node` objects directly:

```python
for element in mesh.elements:
    print(element.tag, element.type, element.node_tags)
    for node in element:
        print(node.coordinates)

quad = mesh.elements[12]
print(quad.nodes)
print(quad.connectivity)
```

Element kinds are `IntEnum` values, so they are descriptive while remaining
compatible with numeric Gmsh IDs:

```python
from gmshparser.api import ElementType

triangles = mesh.elements.by_type(ElementType.TRIANGLE)
assert ElementType.TRIANGLE == 2
assert int(ElementType.QUADRANGLE) == 3
```

Unnamed higher-order or future values remain usable as `TYPE_<id>` enum
pseudo-members.

Filter without traversing entity blocks:

```python
surface_quads = mesh.elements.where(
    element_type=ElementType.QUADRANGLE,
    dimension=2,
)
entity_elements = mesh.elements.where(entity=(2, 7))
print(mesh.element_types)
```

Filtered collections support the same iteration and tag lookup as
`mesh.elements`.

## Unified entities

The modern API combines legacy node and element blocks into one entity view.
Entities are indexed by `(dimension, tag)`:

```python
surface = mesh.entities[(2, 7)]

for node in surface.nodes:
    print(node.tag)

for element in surface.elements:
    print(element.tag, element.type)

print(surface.element_types)
```

Filter entities by their contents:

```python
surfaces = mesh.entities.where(dimension=2)
triangle_entities = mesh.entities.where(element_type=ElementType.TRIANGLE)
entities_with_nodes = mesh.entities.where(has_nodes=True)
```

The separate node-entity and element-entity collections remain only in the
compatibility API.

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
