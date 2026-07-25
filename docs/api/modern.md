# Modern API

The modern API is available through `gmshparser.read()` and `gmshparser.api`. It is immutable, tag-addressable, and intended for application code.

Top-level `gmshparser.parse()` continues to return the compatibility model. `gmshparser.api.parse()` is the modern alias.

## Entry points

::: gmshparser.api.read
    options:
      show_source: true
      heading_level: 3

::: gmshparser.api.parse
    options:
      show_source: true
      heading_level: 3

## Key types

The module defines these tuple aliases:

```python
type EntityKey = tuple[int, int]
type PhysicalGroupKey = tuple[int, int]
type PeriodicLinkKey = tuple[int, int]
```

Each key is `(dimension, tag)`.

## Mesh and metadata

::: gmshparser.api.Mesh
    options:
      show_source: true
      heading_level: 3
      members: true

`Mesh.from_legacy()` explicitly converts an existing compatibility mesh. Normal new code should call `read()` directly.

::: gmshparser.api.Version
    options:
      show_source: true
      heading_level: 3
      members: true

## Element topology

::: gmshparser.api.ElementType
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.ElementFamily
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.ElementTypeInfo
    options:
      show_source: true
      heading_level: 3
      members: true

`ElementType` is an `IntEnum`: known Gmsh IDs have descriptive names, while unknown numeric IDs remain representable as `TYPE_<id>` pseudo-members. Topology metadata is `None` for unknown values.

## Collections

All modern collections preserve parser order. Node and element collections index by original Gmsh tag. Entity, physical-group, and periodic-link collections use `(dimension, tag)` keys.

::: gmshparser.api.NodeCollection
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.ElementCollection
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.EntityCollection
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.PhysicalGroupCollection
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.PeriodicLinkCollection
    options:
      show_source: true
      heading_level: 3
      members: true

## Value objects

::: gmshparser.api.Node
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.Element
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.Entity
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.PhysicalGroup
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.PeriodicLink
    options:
      show_source: true
      heading_level: 3
      members: true

## Related guides

- [Modern Data Model](../user-guide/pythonic-api.md)
- [Working with Meshes](../user-guide/basic-usage.md)
- [Physical Groups and Periodicity](../user-guide/physical-groups.md)
