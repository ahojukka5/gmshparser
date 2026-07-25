# Modern Data Model

`gmshparser.read()` is the recommended entry point for new code. It returns an immutable model built around normal Python attributes, iteration, original Gmsh tags, direct object relationships, and small filtering operations.

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")
```

## Entry points

| Call | Returned model |
| --- | --- |
| `gmshparser.read(source)` | modern immutable model |
| `gmshparser.api.parse(source)` | modern immutable model through the explicit namespace |
| `gmshparser.parse(filename)` | original mutable compatibility model |

Top-level `parse()` intentionally keeps its historical behavior.

## Immutability

Modern values are read-only dataclasses and collections. Parsing produces one coherent object graph that application code can inspect safely without parser mutation leaking into it.

Filtering creates new lightweight collections rather than modifying the mesh:

```python
surface_elements = mesh.elements.where(dimension=2)
```

Use [NumPy Interoperability](numpy.md) when mutable numerical arrays are required.

## Mesh

The mesh owns all application-facing data:

```python
print(mesh.name)
print(mesh.version)
print(mesh.is_ascii)
print(mesh.data_size)
print(mesh.dimension)
print(mesh.bounds)

print(mesh.nodes)
print(mesh.elements)
print(mesh.entities)
print(mesh.physical_groups)
print(mesh.periodic_links)
```

Counts are derived from collections:

```python
print(len(mesh.nodes))
print(len(mesh.elements))
print(len(mesh.entities))
```

## Tags and keys

Node and element collections index by original Gmsh tag:

```python
node = mesh.nodes[42]
element = mesh.elements[17]
```

This is not positional indexing. Use NumPy conversion for zero-based array connectivity.

Entities, physical groups, and periodic links use `(dimension, tag)` keys:

```python
surface = mesh.entities[(2, 7)]
walls = mesh.physical_groups[(2, 10)]
link = mesh.periodic_links[(2, 7)]
```

Convenience methods avoid constructing keys manually:

```python
surface = mesh.entity(dimension=2, tag=7)
link = mesh.periodic_link(dimension=2, tag=7)
```

## Nodes

A `Node` stores Cartesian coordinates, ownership metadata, optional parametric coordinates, and physical assignments.

```python
node = mesh.nodes[42]

print(node.tag)
print(node.coordinates)
print(node.x, node.y, node.z)
print(node.dimension, node.entity_tag)
print(node.entity_key)
print(node.parametric_coordinates)
print(node.is_parametric)
print(node.physical_tags)
```

A node can be unpacked as `(x, y, z)`.

## Elements

An `Element` stores a typed Gmsh element kind and direct references to its nodes.

```python
for element in mesh.elements:
    print(element.tag)
    print(element.element_type)
    print(element.node_tags)
    print(element.entity_key)
    print(element.physical_tags)

    for node in element:
        print(node.coordinates)
```

`element.element_type` is canonical. `element.type` remains an alias for code written against an earlier modern API revision.

## Element types

`ElementType` is an integer enum, so readable names remain compatible with Gmsh numeric IDs.

```python
from gmshparser import ElementType

assert ElementType.TRIANGLE == 2
assert int(ElementType.QUADRANGLE) == 3
```

Known types expose topology metadata:

```python
kind = ElementType.SECOND_ORDER_TRIANGLE

print(kind.family)
print(kind.dimension)
print(kind.order)
print(kind.node_count)
print(kind.primary_node_count)
print(kind.is_linear)
print(kind.is_high_order)
print(kind.is_complete)
```

Unknown numeric values remain representable, but their topology metadata is unavailable.

## Unified entities

The compatibility model stores node and element blocks separately. The modern model combines blocks sharing `(dimension, tag)` into one `Entity`.

```python
surface = mesh.entity(dimension=2, tag=7)

print(surface.nodes)
print(surface.elements)
print(surface.element_types)
print(surface.physical_tags)
```

Dimension views are available as `mesh.points`, `mesh.curves`, `mesh.surfaces`, and `mesh.volumes`.

## Collections

Collections preserve parser order and support:

- iteration
- `len(collection)`
- membership tests
- tag or key lookup
- `get()` with a default
- focused `where()` filters
- convenience selectors such as `by_type()`, `by_entity()`, and `by_dimension()`

See [Working with Meshes](basic-usage.md) for task-oriented examples.

## Physical groups and periodicity

Physical groups resolve names and tags to their entities, elements, and participating nodes. Periodic links retain slave-to-master entity and node relations.

See [Physical Groups and Periodicity](physical-groups.md).

## Text streams

The modern entry points accept paths, `Path` objects, and open text streams:

```python
from io import StringIO

mesh = gmshparser.read(StringIO(msh_text), name="generated.msh")
```

## Compatibility conversion

`gmshparser.api.Mesh.from_legacy()` explicitly converts an existing compatibility mesh. It is supported, but the normal modern path is `gmshparser.read()`, which builds the immutable model directly.

See [Migrating from the Compatibility API](migration.md).
