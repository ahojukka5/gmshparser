# Compatibility API

This page documents the original mutable parser-oriented model returned by `gmshparser.parse()`. It remains supported for existing applications. New code should normally use `gmshparser.read()` and the [modern API](modern.md).

## Mesh

::: gmshparser.mesh.Mesh
    options:
      show_source: true
      heading_level: 3
      members: true

The compatibility mesh mirrors MSH entity blocks and exposes explicit `get_*`, `set_*`, and `add_*` methods.

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")

print(mesh.get_name())
print(mesh.get_version())
print(mesh.get_ascii())
print(mesh.get_number_of_nodes())
print(mesh.get_number_of_elements())
```

## Node blocks and nodes

::: gmshparser.node_entity.NodeEntity
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.node.Node
    options:
      show_source: true
      heading_level: 3
      members: true

```python
for entity in mesh.get_node_entities():
    print(entity.get_dimension(), entity.get_tag())
    for node in entity.get_nodes():
        print(node.get_tag(), node.get_coordinates())
```

Legacy node coordinate tuples may contain Cartesian coordinates followed by parametric coordinates.

## Element blocks and elements

::: gmshparser.element_entity.ElementEntity
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.element.Element
    options:
      show_source: true
      heading_level: 3
      members: true

Element blocks are identified by dimension, elementary entity tag, and element type. Existing two-argument lookup remains available when an entity contains one element type:

```python
entity = mesh.get_element_entity(2, 1)
```

For a mixed entity, provide the element type explicitly:

```python
from gmshparser import ElementType

triangles = mesh.get_element_entity(2, 1, ElementType.TRIANGLE)
quadrangles = mesh.get_element_entity(2, 1, ElementType.QUADRANGLE)
```

The two-argument form raises `KeyError` for an ambiguous mixed entity rather than returning an arbitrary block.

## Format versions

::: gmshparser.version_manager.MshFormatVersion
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.version_manager.VersionManager
    options:
      show_source: true
      heading_level: 3
      members: true

These classes support parser version detection and validation. The modern application model exposes the smaller immutable `gmshparser.api.Version` value.

## Migration

Equivalent modern access is flatter:

```python
modern = gmshparser.read("mesh.msh")

print(modern.name)
print(modern.version)
print(len(modern.nodes))
print(len(modern.elements))
```

See [Migrating from the Compatibility API](../user-guide/migration.md) for a method-by-method mapping.
