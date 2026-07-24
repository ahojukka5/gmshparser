# Helpers API

## `get_triangles()`

::: gmshparser.helpers.get_triangles
    options:
      show_source: true
      heading_level: 3

Returns `(X, Y, triangles)`. Triangle connectivity contains zero-based indices
into `X` and `Y`.

```python
import matplotlib.pyplot as plt
from gmshparser.helpers import get_triangles

X, Y, triangles = get_triangles(mesh)
plt.triplot(X, Y, triangles)
```

Only two-dimensional Gmsh type-2 elements are included.

## `get_quads()`

::: gmshparser.helpers.get_quads
    options:
      show_source: true
      heading_level: 3

Returns `(X, Y, quads)`. Quad connectivity contains zero-based indices into `X`
and `Y`.

```python
from matplotlib.patches import Polygon
from gmshparser.helpers import get_quads

X, Y, quads = get_quads(mesh)
for quad in quads:
    coordinates = [(X[index], Y[index]) for index in quad]
    axes.add_patch(Polygon(coordinates, fill=False))
```

Only two-dimensional Gmsh type-3 elements are included.

## `get_elements_2d()`

::: gmshparser.helpers.get_elements_2d
    options:
      show_source: true
      heading_level: 3

Returns a dictionary rather than coordinate arrays:

```python
from gmshparser.helpers import get_elements_2d

data = get_elements_2d(mesh)

nodes = data["nodes"]
triangles = data["triangles"]
quads = data["quads"]
node_ids = data["node_ids"]
```

- `nodes` maps original Gmsh node tags to `(x, y)` coordinates.
- `triangles` and `quads` preserve original node tags in their connectivity.
- `node_ids` is the sorted list of referenced node tags.

Do not unpack this helper as `(X, Y, triangles, quads)` and do not apply a
`-1` offset to its node tags.

## Line parsers

### `parse_ints()`

Reads one line from a text stream and returns its space-separated values as
integers.

### `parse_floats()`

Reads one line from a text stream and returns its space-separated values as
floating-point numbers.

## See also

- [Visualization](../user-guide/visualization.md)
- [Basic Usage](../user-guide/basic-usage.md)
