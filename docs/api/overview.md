# API Reference

## Package entry points

### `gmshparser.parse()`

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")
```

`parse()` accepts a filename and returns a populated `Mesh`. Supported ASCII MSH
versions are detected automatically.

Typical exceptions include `FileNotFoundError` for a missing file and
`ValueError` for unsupported version metadata. Malformed section contents may
raise conversion or parsing exceptions from the relevant parser.

### Package metadata

```python
import gmshparser

print(gmshparser.__version__)
```

## Data model

- [`Mesh`](mesh.md) stores format metadata, counts, tag ranges, and entity lists.
- `NodeEntity` groups `Node` objects.
- `ElementEntity` groups `Element` objects with a shared Gmsh element type.
- [`MainParser` and section parsers](parsers.md) populate the model.

## Common operations

```python
mesh.get_version()
mesh.is_ascii()
mesh.get_number_of_nodes()
mesh.get_number_of_elements()
```

Iterate over nodes:

```python
for entity in mesh.get_node_entities():
    for node in entity.get_nodes():
        node_id = node.get_tag()
        coordinates = node.get_coordinates()
```

Iterate over elements:

```python
for entity in mesh.get_element_entities():
    element_type = entity.get_element_type()
    for element in entity.get_elements():
        element_id = element.get_tag()
        connectivity = element.get_connectivity()
```

## Helpers

```python
from gmshparser.helpers import get_elements_2d, get_quads, get_triangles

X, Y, triangles = get_triangles(mesh)
X, Y, quads = get_quads(mesh)
mixed = get_elements_2d(mesh)
```

`get_triangles()` and `get_quads()` return zero-based connectivity into their
coordinate arrays. `get_elements_2d()` returns a dictionary with `nodes`,
`triangles`, `quads`, and `node_ids`, preserving original node tags in the
connectivity lists.

See [Helpers API](helpers.md) for examples.
