# Architecture

gmshparser separates version-specific text parsing from its two public data
models. The same section parsers target either the original mutable compatibility
mesh or a direct builder for the immutable modern API.

## Parsing flow

```text
ASCII MSH stream
      │
      ▼
MainParser + version-specific section parsers
      │
      ├────────► compatibility Mesh ────────► gmshparser.parse()
      │
      └────────► ModernMeshBuilder ─────────► gmshparser.read()
                         │
                         └─ immutable api.Mesh
```

`gmshparser.parse(filename)` retains the historical mutable model and behavior.
`gmshparser.read(source)` accepts a path or open text stream and builds the
immutable model directly without first allocating a compatibility `Mesh`.

Because inputs are read in text mode, both paths support ASCII MSH files only.

## Version routing

`MainParser` detects the format and chooses one of these parser lists:

```python
DEFAULT_PARSERS_V1 = [NodesParserV1, ElementsParserV1]
DEFAULT_PARSERS_V2 = [MeshFormatParser, PhysicalNamesParser, NodesParserV2, ElementsParserV2]
DEFAULT_PARSERS_V4 = [
    MeshFormatParser,
    PhysicalNamesParser,
    EntitiesParser,
    NodesParser,
    ElementsParser,
]
```

A leading `$NOD` selects MSH 1.0. `$MeshFormat` is parsed and validated for MSH
2.x and 4.x. MSH 2.0, 2.1, and 2.2 share the V2 parsers; MSH 4.0 and 4.1 share
the V4 parsers.

The main loop dispatches registered section headers to their parser. Optional
sections without a registered parser are not retained.

## Shared parser-target protocol

Section parsers use a small mutable, duck-typed target protocol. It covers:

- mesh format metadata
- declared node and element counts and tag ranges
- node and element entity blocks
- physical names
- entity and element physical tags

The compatibility `mesh.Mesh` and `ModernMeshBuilder` both implement this
protocol. Section parsers therefore contain no public-model branching and retain
identical validation and structured error behavior on both entry points.

The type annotation on older parser methods still names the compatibility
`Mesh`, but parser execution relies only on the shared method protocol.

## Compatibility model

```text
mesh.Mesh
  ├─ NodeEntity[]
  │    └─ Node[]
  └─ ElementEntity[]
       └─ Element[]
```

This mutable model closely follows parser and MSH block structure. It stores
aggregate counts, tag ranges, and explicit `get_*` and `set_*` methods. It is
retained for existing applications and remains the direct target of
`gmshparser.parse()`.

Element blocks are internally distinguished by dimension, elementary entity tag,
and element type, so mixed element types on one entity do not overwrite one
another.

## Direct modern builder

`ModernMeshBuilder` receives the temporary node and element blocks produced by
the existing section parsers. It immediately flattens them into compact raw
records rather than retaining the mutable compatibility object graph.

After parsing, one final indexed build pass:

1. creates immutable `Node` values and a tag-to-node lookup
2. resolves element connectivity directly to those node objects
3. combines node and element blocks into unified `Entity` values
4. indexes entities, elements, and participating nodes by physical group
5. creates the final immutable `api.Mesh`

The builder delays final value creation until all sections have been read. This
is necessary because flat MSH 1.x and 2.x element records can add physical-group
metadata after node records have already been parsed.

The old `api.Mesh.from_legacy()` conversion remains public and supported for
applications that explicitly need to convert a compatibility mesh. It is no
longer part of the normal `read()` path.

## Modern public model

```text
api.Mesh
  ├─ version: Version
  ├─ nodes: NodeCollection
  ├─ elements: ElementCollection
  ├─ entities: EntityCollection
  │      └─ Entity(nodes, elements)
  └─ physical_groups: PhysicalGroupCollection
```

Both the direct builder and `Mesh.from_legacy()` apply the same public-model
rules:

- node and element blocks with the same `(dimension, tag)` become one `Entity`
- each `Element` stores direct references to immutable `Node` objects
- numeric element IDs become `ElementType` integer-enum values
- Cartesian and parametric node coordinates are separated
- MSH versions become a `Version(major, minor)` value
- counts are derived from collections instead of duplicated public metadata

Flat node and element collections are the default access path. Entity context is
retained on each value and through `mesh.entities` when the original grouping
matters.

Collection conventions are intentional:

- iteration yields value objects
- integer indexing uses globally unique Gmsh tags
- entity indexing uses `(dimension, tag)`
- filtering returns a new immutable collection
- elements iterate over their `Node` objects

The compatibility and modern models remain separate so parser mutation cannot
leak into application-facing values.

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
called. `MainParser` wraps it in `SourceTextIO`, which tracks filename, section,
line number, and offending line for structured parser errors.

## Adding section support

A new retained section normally requires:

1. an `AbstractParser` implementation
2. target-protocol methods or metadata storage in both `mesh.Mesh` and
   `ModernMeshBuilder`
3. conversion support in `api.Mesh.from_legacy()` when the compatibility model
   exposes the new data
4. finalization support in `ModernMeshBuilder.build()`
5. registration in each applicable version-specific parser list
6. a small fixture and parity tests for both public entry points
7. updated user and API documentation

## Helpers

`helpers.py` contains line-parsing utilities and visualization adapters. The
visualization functions use a small duck-typed adapter layer and therefore
accept both public mesh models.

## Constraints

- the complete mesh is loaded into memory
- modern values are built eagerly after all supported sections are parsed
- lazy loading and streaming iteration are not implemented
- the library reads but does not write meshes
- binary data and many optional MSH sections are not represented

See [Writing Parsers](writing-parsers.md), [Testing](testing.md),
[Performance benchmarks](benchmarks.md), and the
[API Reference](../api/overview.md).
