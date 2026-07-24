# NumPy interoperability

NumPy support is optional. Install the extra only in projects that need array
interop:

```bash
pip install "gmshparser[numpy]"
```

or with uv:

```bash
uv add "gmshparser[numpy]"
```

The normal `gmshparser` installation remains dependency-free.

## Convert a mesh

```python
import gmshparser
import gmshparser.numpy as gnp

mesh = gmshparser.read("mesh.msh")
arrays = gnp.to_numpy(mesh)
```

The conversion returns detached writable arrays. Editing them does not mutate the
immutable modern mesh.

```python
print(arrays.points.shape)           # (number_of_nodes, 3)
print(arrays.node_tags.shape)        # (number_of_nodes,)
print(arrays.node_entity_keys.shape) # (number_of_nodes, 2)
```

`points[row]` and `node_tags[row]` always describe the same node. The entity key
row contains `(dimension, entity_tag)`.

## Cell blocks

Elements are grouped by `ElementType`. This keeps every connectivity array
rectangular even when the mesh contains lines, triangles, quadrangles, and
volumes at the same time:

```python
from gmshparser import ElementType

triangles = arrays.cells[ElementType.TRIANGLE]

print(triangles.connectivity.shape)
print(triangles.element_tags.shape)
print(triangles.entity_keys.shape)
```

Connectivity contains **zero-based row indices into `arrays.points`**, not Gmsh
node tags. This is the representation expected by most NumPy algorithms:

```python
triangle_points = arrays.points[triangles.connectivity]
```

Original Gmsh node tags can be reconstructed with the matching shape:

```python
triangle_node_tags = arrays.cell_node_tags(ElementType.TRIANGLE)
```

Each cell block also reports:

```python
print(triangles.element_type)
print(triangles.number_of_elements)
print(triangles.nodes_per_element)
```

The `cells` mapping is read-only so element-type keys cannot accidentally be
replaced. The contained arrays are normal writable NumPy arrays.

## Select element types

Keep all points but convert only selected element types:

```python
arrays = gnp.to_numpy(
    mesh,
    element_types=[ElementType.TRIANGLE, ElementType.QUADRANGLE],
)
```

Keeping the full point table means row indices remain stable across filtered
conversions.

## Choose dtypes

Coordinates default to `float64`; tags, entity keys, and connectivity default to
`int64`. Both are configurable:

```python
import numpy as np

arrays = gnp.to_numpy(
    mesh,
    coordinate_dtype=np.float32,
    index_dtype=np.int32,
)
```

`index_dtype` must be an integer NumPy dtype.

## Compatibility model

The converter intentionally accepts only the modern model returned by
`gmshparser.read()` or `gmshparser.api.parse()`. Existing applications using the
mutable compatibility model can keep using that API, or switch their entry point
to `read()` before array conversion.
