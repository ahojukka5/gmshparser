# Architecture

gmshparser separates parsing from the recommended public data model. Section
parsers continue to populate the original mutable compatibility model, and the
modern API converts that result into immutable application-facing value objects.

## Parsing flow

Both public entry points use the same section parsers:

```text
ASCII MSH stream
      │
      ▼
MainParser + version-specific section parsers
      │
      ▼
mutable compatibility Mesh
      ├──────────────► gmshparser.parse()
      │
      └─ conversion ─► gmshparser.read() / gmshparser.api.Mesh
```

`gmshparser.parse(filename)` returns the mutable compatibility model directly.
`gmshparser.read(source)` accepts a path or open text stream, runs the same
parsers, and converts the populated model into the immutable modern model.

Because inputs are read in text mode, the implementation supports ASCII MSH
files only.

## Version routing

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
sections without a registered parser are not retained.

## Compatibility model

```text
mesh.Mesh
  ├─ NodeEntity[]
  │    └─ Node[]
  └─ ElementEntity[]
       └─ Element[]
```

This mutable model closely follows parser and MSH block structure. It stores
aggregate counts, tag ranges, and uses explicit `get_*` and `set_*` methods. It
is retained to avoid breaking existing applications and remains the target that
section parsers populate.

## Modern public model

```text
api.Mesh
  ├─ version: Version
  ├─ nodes: NodeCollection
  ├─ elements: ElementCollection
  └─ entities: EntityCollection
         └─ Entity(nodes, elements)
```

The conversion in `api.Mesh.from_legacy()` deliberately removes parser-oriented
structure:

- node and element blocks with the same `(dimension, tag)` become one `Entity`
- each `Element` stores direct references to its immutable `Node` objects
- numeric element IDs become `ElementType` integer-enum values
- Cartesian and parametric node coordinates are separated
- MSH versions become a `Version(major, minor)` value
- counts are derived from collections instead of duplicated metadata

Flat node and element collections are the default access path. Entity context is
retained on each value and through `mesh.entities` when the original grouping
matters.

Collection conventions are intentional:

- iteration yields value objects
- integer indexing uses globally unique Gmsh tags
- entity indexing uses `(dimension, tag)`
- filtering returns a new immutable collection
- elements iterate over their `Node` objects

The compatibility and modern models are separate so parser mutation cannot leak
into application-facing values.

## Version management

The parser layer uses `MshFormatVersion` and `VersionManager` to validate input.
The public model exposes the smaller immutable `api.Version` value with `major`
and `minor` attributes.

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
2. compatibility-model changes for parser storage
3. conversion changes in `api.Mesh.from_legacy()` for modern exposure
4. registration in each applicable version-specific parser list
5. a small fixture and focused tests for both public entry points
6. updated user and API documentation

## Helpers

`helpers.py` contains line-parsing utilities and visualization adapters. The
visualization functions use a small duck-typed adapter layer and therefore
accept both public mesh models.

## Constraints

- the complete mesh is loaded into memory
- the modern API performs an eager conversion after parsing
- lazy loading and streaming iteration are not implemented
- the library reads but does not write meshes
- binary data and many optional MSH sections are not represented

See [Writing Parsers](writing-parsers.md), [Testing](testing.md), and the
[API Reference](../api/overview.md).
