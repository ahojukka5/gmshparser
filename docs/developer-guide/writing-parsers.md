# Writing Parsers

A section parser reads one complete MSH section and stores its data in a `Mesh`
or a related compatibility-model object.

## Parser contract

A parser implements `AbstractParser` and provides two static methods:

```python
from typing import TextIO

from gmshparser.abstract_parser import AbstractParser
from gmshparser.mesh import Mesh


class ExampleParser(AbstractParser):
    @staticmethod
    def get_section_name() -> str:
        return "$Example"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        ...
```

`MainParser` normally consumes the opening section marker before `parse()` is
called. A section parser must then:

1. read and validate the complete payload
2. verify declared record counts
3. consume and validate its `$End...` marker
4. stop immediately after the end marker

Some existing parsers also accept a stream positioned at their opening marker so
they can be tested directly. Preserve that behavior when modifying such a parser.

## Required reads and end markers

Use the shared parsing helpers instead of calling `readline()` for mandatory
records:

```python
from gmshparser.parsing import expect_end_marker, read_required_line

line = read_required_line(io, "an $Example record")
...
expect_end_marker(io, "$EndExample")
```

`read_required_line()` raises `UnexpectedEndOfFileError` when the stream ends
inside a declared section. `expect_end_marker()` reports both a missing marker
and an unexpected line with the current source context.

## Example parser

```python
from gmshparser.errors import InvalidSectionError
from gmshparser.parsing import expect_end_marker, read_required_line


class ExampleParser(AbstractParser):
    @staticmethod
    def get_section_name() -> str:
        return "$Example"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        count_line = read_required_line(io, "$Example count")
        try:
            count = int(count_line)
        except ValueError as error:
            raise InvalidSectionError(
                "$Example count must be an integer"
            ) from error

        if count < 0:
            raise InvalidSectionError("$Example count cannot be negative")

        for _ in range(count):
            record = read_required_line(io, "an $Example record")
            ...

        expect_end_marker(io, "$EndExample")
```

Do not print parser failures. `MainParser` attaches the filename, current line
number, section, and source line to `ParseError` subclasses. Applications decide
how exceptions are logged or displayed.

## Choose a specific error type

Use the most specific public exception that describes the malformed input:

- `InvalidSectionError` for headers, counts, generic records, and end markers
- `InvalidNodeError` for node blocks and node records
- `InvalidElementError` for element blocks and element records
- `InvalidElementConnectivityError` for connectivity width mismatches
- `UnknownElementTypeError` when topology metadata is required but unavailable
- `UnsupportedVersionError` and `UnsupportedBinaryFormatError` for format limits

All parser errors inherit from both `ParseError` and `ValueError`.

## Register the parser

The parser registries are version-specific:

```python
DEFAULT_PARSERS_V1
DEFAULT_PARSERS_V2
DEFAULT_PARSERS_V4
```

Register a parser only for formats where its section layout applies. A parser
shared by MSH 2.x and 4.x is added to both lists:

```python
DEFAULT_PARSERS_V2 = [
    MeshFormatParser,
    PhysicalNamesParser,
    NodesParserV2,
    ElementsParserV2,
]

DEFAULT_PARSERS_V4 = [
    MeshFormatParser,
    PhysicalNamesParser,
    EntitiesParser,
    NodesParser,
    ElementsParser,
]
```

Do not add a single `DEFAULT_PARSERS` list: the implementation does not use one.

For specialized callers, `MainParser(parsers=[...])` accepts an explicit parser
list. That list replaces automatic version-specific selection, so it must
contain every section parser needed by the input.

## Version-specific layouts

When the same section has different layouts, prefer separate parser classes:

```python
class ExampleParserV2(AbstractParser):
    @staticmethod
    def get_section_name() -> str:
        return "$Example"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        ...


class ExampleParserV4(AbstractParser):
    @staticmethod
    def get_section_name() -> str:
        return "$Example"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        ...
```

Register each class in the matching parser list. This follows the existing
`NodesParserV2`/`NodesParser` and `ElementsParserV2`/`ElementsParser` split.

## Testing checklist

- add the smallest complete valid section fixture, including its end marker
- verify the values exposed through the public data model
- cover each applicable MSH version family
- test malformed headers and numeric fields
- test truncated payloads and missing end markers
- verify the specific exception class and source-context attributes
- ensure an unrelated optional section remains harmless
- run Ruff, pytest, and the documentation build

```bash
uv run ruff format --check gmshparser tests examples
uv run ruff check gmshparser tests examples
uv run pytest
uv sync --group docs
uv run mkdocs build
```

## Documentation checklist

Update:

- [Supported Formats](../user-guide/supported-formats.md) when support changes
- [Error Handling](../user-guide/error-handling.md) for new public failures
- [Architecture](architecture.md) when routing or data-model structure changes
- the API reference for new public model methods, parsers, or exceptions
- the changelog for user-visible releases
