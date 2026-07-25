# Package API

The top-level `gmshparser` namespace contains the supported entry points, modern value types, structured errors, element metadata, and compatibility aliases most applications need.

## Entry points

::: gmshparser.read
    options:
      show_source: true
      heading_level: 3

::: gmshparser.parse
    options:
      show_source: true
      heading_level: 3

`read()` returns the modern immutable `gmshparser.api.Mesh`. `parse()` retains the original mutable `gmshparser.mesh.Mesh` behavior.

## Package metadata

`gmshparser.__version__` is read from the installed distribution metadata. `gmshparser.__author__` identifies the package author.

```python
import gmshparser

print(gmshparser.__version__)
```

## Top-level modern exports

The following modern types are available directly from `gmshparser` and canonically defined in `gmshparser.api`:

- `ModernMesh`
- `Version`
- `Node` and `NodeCollection`
- `Element` and `ElementCollection`
- `Entity` and `EntityCollection`
- `PhysicalGroup` and `PhysicalGroupCollection`
- `PeriodicLink` and `PeriodicLinkCollection`

See [Modern API](modern.md) for their complete members.

## Element metadata

The top-level namespace exports `ElementType`, `ElementFamily`, and `ElementTypeInfo`. They are documented with the modern model because elements and collection filters use them throughout the public API.

## Errors

All public parser errors are available directly from `gmshparser`, including `ParseError` and its specialized subclasses. See [Errors](errors.md).

## Compatibility exports

`gmshparser.Mesh` is the original mutable model. `gmshparser.MainParser`, `gmshparser.MshFormatVersion`, and `gmshparser.VersionManager` remain available for compatibility and parser development. See [Compatibility API](mesh.md) and [Parser Internals](../developer-guide/parser-internals.md).

## Submodules

- `gmshparser.api` — modern immutable model and modern `parse()` alias
- `gmshparser.numpy` — optional NumPy conversion
- `gmshparser.helpers` — 2D visualization adapters and line parsers
- `gmshparser.errors` — structured error hierarchy
