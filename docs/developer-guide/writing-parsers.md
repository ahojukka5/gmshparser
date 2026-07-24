# Writing Parsers

A section parser reads one MSH section and stores its data in a `Mesh` or a
related model object.

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

`MainParser` has already consumed the section header when `parse()` is called.
The section parser should read exactly the section payload. The main loop can
then consume and ignore the `$End...` line.

## Example: physical names

gmshparser does not currently retain `$PhysicalNames`. Adding it requires both
a parser and a place in the data model to store the result.

```python
class PhysicalNamesParser(AbstractParser):
    @staticmethod
    def get_section_name() -> str:
        return "$PhysicalNames"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        count = int(io.readline().strip())
        names = {}

        for _ in range(count):
            dimension, tag, quoted_name = io.readline().split(maxsplit=2)
            names[(int(dimension), int(tag))] = quoted_name.strip().strip('"')

        mesh.set_physical_names(names)
```

This example assumes that `Mesh` has matching `set_physical_names()` and
`get_physical_names()` methods. Add and test those methods as part of the same
change.

## Register the parser

The current parser registries are version-specific:

```python
DEFAULT_PARSERS_V1
DEFAULT_PARSERS_V2
DEFAULT_PARSERS_V4
```

Register the new parser only for formats where the section layout applies. For
example, a parser shared by MSH 2.x and 4.x would be added to both lists:

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

## Error handling

Validate section counts and record structure close to where they are read:

```python
line = io.readline()
if not line:
    raise ValueError("Unexpected end of file in $Example")

try:
    count = int(line)
except ValueError as error:
    raise ValueError(f"Invalid $Example count: {line.strip()}") from error

if count < 0:
    raise ValueError("$Example count cannot be negative")
```

Avoid silently inventing defaults for malformed mandatory fields.

## Testing checklist

- add the smallest valid section fixture
- verify the values exposed through the public data model
- cover each applicable MSH version family
- add malformed-input tests when the parser performs validation
- ensure an unrelated optional section remains harmless
- run Black, flake8, pytest, and the documentation build

```bash
uv run black . --check
uv run flake8 gmshparser tests
uv run pytest
uv sync --group docs
uv run mkdocs build
```

## Documentation checklist

Update:

- [Supported Formats](../user-guide/supported-formats.md) when support changes
- [Architecture](architecture.md) when routing or data-model structure changes
- the API reference for new public model methods or parser classes
- the changelog for user-visible releases
