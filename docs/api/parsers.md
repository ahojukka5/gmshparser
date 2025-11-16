# Parsers API

## AbstractParser

Base class for all parsers.

::: gmshparser.abstract_parser.AbstractParser
    options:
      show_source: true
      heading_level: 3

## MeshFormatParser

Parses `$MeshFormat` section.

## NodesParser

Parses `$Nodes` section (MSH 2.x and 4.x).

## ElementsParser

Parses `$Elements` section (MSH 2.x and 4.x).

## V1 Parsers

### NodesParserV1

Parses `$NOD` section (MSH 1.0).

### ElementsParserV1

Parses `$ELM` section (MSH 1.0).

## MainParser

Coordinates all parsers and handles version detection.

::: gmshparser.main_parser.MainParser
    options:
      show_source: true
      heading_level: 3

## See Also

- [Writing Custom Parsers](../developer-guide/writing-parsers.md)
- [Architecture](../developer-guide/architecture.md)
