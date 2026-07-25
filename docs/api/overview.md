# API Reference

This reference documents the supported Python surface of gmshparser. Tutorials and task-oriented examples belong in the [User Guide](../user-guide/index.md); parser implementation details belong in the [Developer Guide](../developer-guide/index.md).

## Entry points

| Call | Return type | Intended use |
| --- | --- | --- |
| `gmshparser.read(source, *, name=None)` | `gmshparser.api.Mesh` | recommended for new code |
| `gmshparser.api.parse(source, *, name=None)` | `gmshparser.api.Mesh` | modern alias for users who prefer `parse` |
| `gmshparser.parse(filename)` | `gmshparser.mesh.Mesh` | existing compatibility applications |

See [Package API](package.md) for top-level exports.

## Reference sections

- [Modern API](modern.md) — immutable mesh, nodes, elements, entities, physical groups, periodic links, collections, and element metadata.
- [NumPy API](numpy.md) — detached point arrays and element-type cell blocks.
- [Errors](errors.md) — structured parser exceptions and source context.
- [Compatibility API](mesh.md) — original mutable mesh, entity blocks, nodes, elements, and version helpers.
- [Helpers](helpers.md) — visualization adapters and low-level line parsers.

## Public versus internal APIs

The modern model, top-level entry points, errors, element metadata, NumPy conversion, helpers, and compatibility classes are documented here because applications may use them directly.

Version-specific section parsers and parser registries are development interfaces. They are documented under [Parser Internals](../developer-guide/parser-internals.md), not mixed into the application API reference.

## Conventions

- Integer collection indexing uses original Gmsh tags, not positional offsets.
- Entity, physical-group, and periodic-link keys are `(dimension, tag)` tuples.
- Modern values and collections are immutable.
- Compatibility values remain mutable and use `get_*` / `set_*` methods.
- Both entry points raise the same structured parser errors.

For a guided introduction, start with [Getting Started](../user-guide/getting-started.md) and [Modern Data Model](../user-guide/pythonic-api.md).
