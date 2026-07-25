# Parser Internals

This page documents the parser classes used inside gmshparser. They are exposed for compatibility and development, but application code should normally use `gmshparser.read()` or `gmshparser.parse()`.

## Main dispatch

::: gmshparser.main_parser.MainParser
    options:
      show_source: true
      heading_level: 3
      members: true

`MainParser` detects the MSH version, selects a version-specific parser registry, and dispatches recognized section headers. Unknown sections are skipped.

## Parser interface

::: gmshparser.abstract_parser.AbstractParser
    options:
      show_source: true
      heading_level: 3
      members: true

Section parsers receive a mutable parser target and a text stream positioned immediately after the section header. The compatibility `Mesh` and `ModernMeshBuilder` implement the shared target operations.

## Common sections

::: gmshparser.mesh_format_parser.MeshFormatParser
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.physical_names_parser.PhysicalNamesParser
    options:
      show_source: true
      heading_level: 3
      members: true

## MSH 1.0

::: gmshparser.nodes_parser_v1.NodesParserV1
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.elements_parser_v1.ElementsParserV1
    options:
      show_source: true
      heading_level: 3
      members: true

## MSH 2.x

::: gmshparser.nodes_parser_v2.NodesParserV2
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.elements_parser_v2.ElementsParserV2
    options:
      show_source: true
      heading_level: 3
      members: true

## MSH 4.x

::: gmshparser.entities_parser.EntitiesParser
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.nodes_parser.NodesParser
    options:
      show_source: true
      heading_level: 3
      members: true

::: gmshparser.elements_parser.ElementsParser
    options:
      show_source: true
      heading_level: 3
      members: true

## Version registries

The parser lists are defined in `gmshparser.main_parser`:

```python
DEFAULT_PARSERS_V1
DEFAULT_PARSERS_V2
DEFAULT_PARSERS_V4
```

Add a section parser only to the format families whose record layout it understands. See [Writing Parsers](writing-parsers.md) for the implementation and test checklist.
