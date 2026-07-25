# Modern API Reference

The modern API is available through `gmshparser.read()` and the value objects in
`gmshparser.api`. The equivalent `gmshparser.api.parse()` name is provided inside
the explicit modern namespace. Top-level `gmshparser.parse()` continues to
return the original compatibility model.

## Entry points

::: gmshparser.api.read
    options:
      show_source: true
      heading_level: 3

::: gmshparser.api.parse
    options:
      show_source: true
      heading_level: 3

## Mesh and metadata

::: gmshparser.api.Mesh
    options:
      show_source: true
      heading_level: 3
      members: true

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

## Collections

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

::: gmshparser.api.PeriodicLinkCollection
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.PhysicalGroupCollection
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

::: gmshparser.api.PeriodicLink
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.api.PhysicalGroup
    options:
      show_source: true
      heading_level: 3
      members: true
