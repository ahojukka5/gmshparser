# API Reference

## Recommended entry point

### `gmshparser.read()`

```python
import gmshparser
from gmshparser.api import ElementType

mesh = gmshparser.read("mesh.msh")
```

`read()` returns the modern immutable model from `gmshparser.api`. It accepts a
filesystem path or an open text stream.

```python
for node in mesh.nodes:
    print(node.tag, node.coordinates)

triangles = mesh.elements.by_type(ElementType.TRIANGLE)
element = mesh.elements[17]
entity = mesh.entities[(2, 7)]
```

The modern model provides:

- normal attributes instead of `get_*` methods
- flat, tag-addressable node and element collections
- direct `Element` → `Node` relationships
- typed `ElementType` values
- unified entities containing both nodes and elements
- filtering by element type, dimension, entity, and contents
- immutable application-facing value objects

See the [Modern API reference](modern.md) and
[Pythonic API guide](../user-guide/pythonic-api.md).

## Compatibility entry point

### `gmshparser.parse()`

```python
legacy_mesh = gmshparser.parse("mesh.msh")
```

`parse()` retains the original mutable parser-oriented data model and its
`get_*` / `set_*` methods. Existing applications can continue using it without
changes. The compatibility classes are documented under
[Compatibility Mesh](mesh.md) and [Parsers](parsers.md).

## Package metadata

```python
import gmshparser

print(gmshparser.__version__)
```

## Helpers

Visualization helpers accept either mesh model:

```python
X, Y, triangles = gmshparser.helpers.get_triangles(mesh)
X, Y, quads = gmshparser.helpers.get_quads(mesh)
mixed = gmshparser.helpers.get_elements_2d(mesh)
```

`get_triangles()` and `get_quads()` return zero-based connectivity into their
coordinate arrays. `get_elements_2d()` preserves original Gmsh node tags in its
connectivity lists.
