# Migrating from the Compatibility API

The compatibility API remains supported. Migration is optional and can be done one call site at a time.

## Change the entry point

Compatibility model:

```python
legacy_mesh = gmshparser.parse("mesh.msh")
```

Modern model:

```python
mesh = gmshparser.read("mesh.msh")
```

Top-level `gmshparser.parse()` intentionally keeps its historical behavior. `gmshparser.api.parse()` is an alias for the modern reader when an application prefers the verb `parse`.

## Common replacements

| Compatibility API | Modern API |
| --- | --- |
| `mesh.get_name()` | `mesh.name` |
| `mesh.get_version()` | `mesh.version` |
| `mesh.get_ascii()` | `mesh.is_ascii` |
| `mesh.get_precision()` | `mesh.data_size` |
| `mesh.get_number_of_nodes()` | `len(mesh.nodes)` |
| `mesh.get_number_of_elements()` | `len(mesh.elements)` |
| `mesh.get_node_entities()` | `mesh.entities` or `mesh.nodes` |
| `mesh.get_element_entities()` | `mesh.entities` or `mesh.elements` |
| `node.get_tag()` | `node.tag` |
| `node.get_coordinates()` | `node.coordinates` |
| `element.get_tag()` | `element.tag` |
| `element.get_connectivity()` | `element.node_tags` |

## Flatten entity-block loops

Compatibility code often traverses parser blocks:

```python
for entity in legacy_mesh.get_node_entities():
    for node in entity.get_nodes():
        print(node.get_tag(), node.get_coordinates())
```

The modern model exposes a flat node collection:

```python
for node in mesh.nodes:
    print(node.tag, node.coordinates)
```

Entity information is still available when needed:

```python
surface = mesh.entity(dimension=2, tag=7)
print(surface.nodes)
print(surface.elements)
```

## Connectivity

Compatibility elements store node tags as integers. Modern elements resolve those tags to `Node` objects while retaining the original tag tuple.

```python
for element in mesh.elements:
    print(element.node_tags)
    for node in element:
        print(node.coordinates)
```

## Mutability

The compatibility model has `set_*` methods because parsers build it incrementally. The modern model is immutable. Derive new application data instead of modifying the parsed mesh.

```python
selected = mesh.elements.where(dimension=2)
coordinates = tuple(node.coordinates for node in mesh.nodes)
```

NumPy conversion returns detached writable arrays when mutable numerical data is needed.

## Convert an existing compatibility mesh

`gmshparser.api.Mesh.from_legacy()` converts an already parsed compatibility mesh explicitly:

```python
from gmshparser.api import Mesh

modern = Mesh.from_legacy(legacy_mesh)
```

Normal new code should call `gmshparser.read()` directly. It builds the modern model without first allocating the compatibility object graph.

## Error handling

Both entry points expose the same structured `ParseError` hierarchy, so error handlers can usually remain unchanged during migration.

See [Modern Data Model](pythonic-api.md), [Working with Meshes](basic-usage.md), and the [Compatibility API reference](../api/mesh.md).
