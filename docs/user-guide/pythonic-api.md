# Pythonic API

`gmshparser.read()` is the recommended entry point for new code. It returns an
immutable model built around normal Python attributes, iteration, tag lookup,
direct object relationships, physical groups, and small filtering operations.

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")
```

The entry points are deliberately separated:

| Call | Returned model |
| --- | --- |
| `gmshparser.parse(path)` | original mutable compatibility model |
| `gmshparser.read(path)` | modern immutable model |
| `gmshparser.api.parse(path)` | modern immutable model through the explicit modern namespace |

Existing applications using top-level `parse()` therefore remain unchanged.
Users who prefer the verb `parse` for new code can write:

```python
from gmshparser.api import parse

mesh = parse("mesh.msh")
```

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
print(len(mesh.physical_groups))
print(len(mesh.periodic_links))
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
entity_nodes = mesh.nodes.by_entity(dimension=2, tag=7)
physical_nodes = mesh.nodes.where(physical_tag=10)
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
    print(element.tag, element.element_type, element.node_tags)
    for node in element:
        print(node.coordinates)

quad = mesh.elements[12]
print(quad.nodes)
print(quad.connectivity)
```

`element.element_type` is the canonical name. `element.type` remains an alias for
code written against the first version of the modern API.

Element kinds are `IntEnum` values, so they are descriptive while remaining
compatible with numeric Gmsh IDs:

```python
from gmshparser import ElementType

triangles = mesh.elements.by_type(ElementType.TRIANGLE)
assert ElementType.TRIANGLE == 2
assert int(ElementType.QUADRANGLE) == 3
```

The element type registry exposes topology metadata without separate lookup
tables:

```python
kind = ElementType.SECOND_ORDER_TRIANGLE

print(kind.family)              # triangle
print(kind.dimension)           # 2
print(kind.order)               # 2
print(kind.node_count)          # 6
print(kind.primary_node_count)  # 3
print(kind.is_linear)           # False
print(kind.is_high_order)       # True
print(kind.is_complete)         # True
```

The same information is available directly from an element through
`element.info`, `element.family`, `element.order`, `element.expected_node_count`,
`element.primary_node_count`, `element.is_linear`, `element.is_high_order`, and
`element.is_complete`.

Unknown numeric values remain usable as `TYPE_<id>` enum pseudo-members, with
metadata properties set to `None`. Parsers reject types whose topology is needed
but unknown instead of silently guessing their dimension.

Filter without traversing entity blocks:

```python
surface_quads = mesh.elements.where(
    element_type=ElementType.QUADRANGLE,
    dimension=2,
)
entity_elements = mesh.elements.by_entity(dimension=2, tag=7)
physical_elements = mesh.elements.where(physical_tag=10)
print(mesh.element_types)
```

Filtered collections support the same iteration and tag lookup as
`mesh.elements`.

## Unified entities

The modern API combines legacy node and element blocks into one entity view.
Entities remain indexable by `(dimension, tag)`, but normal code can avoid tuple
keys:

```python
surface = mesh.entity(dimension=2, tag=7)

for node in surface.nodes:
    print(node.tag)

for element in surface.elements:
    print(element.tag, element.element_type)

print(surface.element_types)
print(surface.physical_tags)
```

Dimension-specific views are available directly:

```python
print(mesh.points)
print(mesh.curves)
print(mesh.surfaces)
print(mesh.volumes)
```

Collections can also be filtered explicitly:

```python
surfaces = mesh.entities.by_dimension(2)
triangle_entities = mesh.entities.where(element_type=ElementType.TRIANGLE)
entities_with_nodes = mesh.entities.where(has_nodes=True)
physical_entities = mesh.entities.where(physical_tag=10)
```

The separate node-entity and element-entity collections remain only in the
compatibility API.

## Physical groups

Physical group declarations and assignments are preserved from:

- MSH 1.x element region fields
- MSH 2.x element tags and `$PhysicalNames`
- MSH 4.x `$Entities` and `$PhysicalNames`

Look up a group by an unambiguous name or by `(dimension, tag)`:

```python
walls = mesh.physical_groups["Walls"]
domain = mesh.physical_groups[(3, 2)]
```

Each group resolves its entities, elements, and participating nodes:

```python
print(walls.dimension, walls.tag, walls.name)
print(walls.entities)
print(walls.elements)
print(walls.nodes)
```

The mesh convenience method accepts either a name or a numeric tag:

```python
walls = mesh.physical_group("Walls")
domain = mesh.physical_group(2, dimension=3)
```

A numeric tag can be used without `dimension=` only when it identifies exactly
one group. Names that occur in more than one dimension must be addressed by their
`(dimension, tag)` key.

Physical group node collections follow the original mesh node order. This keeps
array and connectivity conversion deterministic.

## Periodic links

MSH 2.x and 4.x `$Periodic` sections are represented as immutable slave-to-master
entity relations:

```python
link = mesh.periodic_links[(2, 7)]
link = mesh.periodic_link(dimension=2, tag=7)

print(link.master_entity_tag)
print(link.affine_transform)
for slave_node_tag, master_node_tag in link.node_pairs:
    print(slave_node_tag, master_node_tag)
```

Collections preserve file order and can be filtered with
`mesh.periodic_links.by_dimension(2)`. Empty affine transformations remain empty;
MSH 4.x affine values and legacy MSH 2.x `Affine` records are retained verbatim as
floating-point tuples.

## Read from a text stream

Both modern entry points accept open text streams in addition to paths:

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

Top-level `parse()` and the mutable parser-oriented classes are retained. New
applications should prefer `read()` or the explicit `gmshparser.api.parse()`
alias and the classes in `gmshparser.api`.
