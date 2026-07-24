# Parsers API

## `AbstractParser`

::: gmshparser.abstract_parser.AbstractParser
    options:
      show_source: true
      heading_level: 3

Section parsers expose a section name and a static `parse(mesh, io)` method.

## `MainParser`

::: gmshparser.main_parser.MainParser
    options:
      show_source: true
      heading_level: 3

`MainParser` detects the MSH version and selects one of the version-specific
parser registries.

## Format metadata

### `MeshFormatParser`

Parses `$MeshFormat`, validates the version, and records the ASCII flag and data
precision. MSH 1.0 does not contain this section.

## MSH 1.0 parsers

### `NodesParserV1`

Parses the legacy `$NOD` section.

### `ElementsParserV1`

Parses the legacy `$ELM` section.

## MSH 2.x parsers

### `NodesParserV2`

Parses the flat `$Nodes` layout used by MSH 2.0, 2.1, and 2.2.

### `ElementsParserV2`

Parses the flat `$Elements` layout used by MSH 2.0, 2.1, and 2.2. It groups
records into `ElementEntity` objects using the elementary entity tag when
available. The complete MSH 2.x element-tag list is not exposed by the current
model.

## MSH 4.x parsers

### `NodesParser`

Parses the entity-block `$Nodes` layout used by MSH 4.0 and 4.1.

### `ElementsParser`

Parses the entity-block `$Elements` layout used by MSH 4.0 and 4.1.

## Parser registries

The default registries are defined in `gmshparser.main_parser`:

```python
DEFAULT_PARSERS_V1
DEFAULT_PARSERS_V2
DEFAULT_PARSERS_V4
```

See [Writing Parsers](../developer-guide/writing-parsers.md) before adding or
registering a new section parser.
