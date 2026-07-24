# Architecture

gmshparser is a read-only parser built around a shared mesh model and separate
section parsers for the supported MSH version families.

## Parsing flow

`gmshparser.parse(filename)` creates a `Mesh`, opens the file in text mode, and
calls `MainParser.parse(mesh, stream)`. The populated `Mesh` is then returned.
Because files are opened as text, the current implementation supports ASCII MSH
files only.

`MainParser` detects the format and chooses one of these parser lists:

```python
DEFAULT_PARSERS_V1 = [NodesParserV1, ElementsParserV1]
DEFAULT_PARSERS_V2 = [MeshFormatParser, NodesParserV2, ElementsParserV2]
DEFAULT_PARSERS_V4 = [MeshFormatParser, NodesParser, ElementsParser]
```

A leading `$NOD` selects MSH 1.0. `$MeshFormat` is parsed and validated for MSH
2.x and 4.x. MSH 2.0, 2.1, and 2.2 share the V2 parsers; MSH 4.0 and 4.1 share
the V4 parsers.

The main loop dispatches registered section headers to their parser. Optional
sections without a registered parser are not retained by the data model.

## Data model

```text
Mesh
  ├─ NodeEntity[]
  │    └─ Node[]
  └─ ElementEntity[]
       └─ Element[]
```

`Mesh` stores format metadata, aggregate counts, tag ranges, and entity lists.
A `Node` stores a tag and coordinates. A `NodeEntity` groups nodes. An `Element`
stores a tag and connectivity. An `ElementEntity` groups elements with a shared
dimension, entity tag, and Gmsh element type.

Legacy and flat formats are normalized into the same entity-based API used for
MSH 4.x.

## Version management

`MshFormatVersion` enumerates MSH 1.0, 2.0, 2.1, 2.2, 4.0, and 4.1.
`VersionManager` parses version strings, validates support, and provides helpers
for the 1.x, 2.x, and 4.x families.

## Parser interface

Section parsers implement `AbstractParser`:

```python
class AbstractParser:
    @staticmethod
    def get_section_name():
        ...

    @staticmethod
    def parse(mesh, io):
        ...
```

The stream is positioned immediately after the section header when `parse()` is
called.

## Adding section support

A new section normally requires:

1. an `AbstractParser` implementation
2. data-model changes when values must be exposed
3. registration in each applicable version-specific parser list
4. a small fixture and focused tests
5. updated user and API documentation

The public `gmshparser.parse()` uses the default registries. `MainParser` also
accepts an explicit parser list for specialized use.

## Helpers

`helpers.py` contains line-parsing utilities and visualization adapters.
`get_triangles()` and `get_quads()` return zero-based plotting connectivity.
`get_elements_2d()` returns a dictionary that preserves original Gmsh node tags.

## Constraints

- the complete mesh is loaded into memory
- lazy loading and streaming are not implemented
- the library reads but does not write meshes
- binary data and many optional MSH sections are not represented

See [Writing Parsers](writing-parsers.md), [Testing](testing.md), and the
[API Reference](../api/overview.md).
