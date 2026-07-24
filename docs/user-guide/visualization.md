# Visualization

gmshparser itself has no plotting dependency. The helper functions in
`gmshparser.helpers` prepare 2D mesh data for optional matplotlib use and accept
both modern `read()` meshes and compatibility `parse()` meshes.

Install matplotlib:

```bash
uv add matplotlib
```

For a repository checkout:

```bash
uv sync --group visualization
```

## Triangular meshes

`get_triangles()` returns `(X, Y, T)`, where `T` contains zero-based indices
into `X` and `Y`:

```python
import gmshparser
import matplotlib.pyplot as plt

mesh = gmshparser.read("mesh.msh")
X, Y, triangles = gmshparser.helpers.get_triangles(mesh)

plt.triplot(X, Y, triangles, color="black", linewidth=0.5)
plt.axis("equal")
plt.show()
```

Only three-node triangular elements are included.

## Quadrilateral meshes

`get_quads()` also returns zero-based connectivity:

```python
import gmshparser
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

mesh = gmshparser.read("quad_mesh.msh")
X, Y, quads = gmshparser.helpers.get_quads(mesh)

figure, axes = plt.subplots()
for quad in quads:
    coordinates = [(X[index], Y[index]) for index in quad]
    axes.add_patch(Polygon(coordinates, fill=False, edgecolor="black"))

axes.autoscale_view()
axes.set_aspect("equal")
plt.show()
```

Only four-node quadrilateral elements are included.

## Mixed triangle and quadrilateral meshes

`get_elements_2d()` returns a dictionary and retains original Gmsh node tags in
the connectivity lists.

```python
import gmshparser
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

mesh = gmshparser.read("mixed_mesh.msh")
data = gmshparser.helpers.get_elements_2d(mesh)

nodes = data["nodes"]
triangles = data["triangles"]
quads = data["quads"]

figure, axes = plt.subplots()

for triangle in triangles:
    coordinates = [nodes[node_tag] for node_tag in triangle]
    axes.add_patch(Polygon(coordinates, fill=False, edgecolor="black"))

for quad in quads:
    coordinates = [nodes[node_tag] for node_tag in quad]
    axes.add_patch(Polygon(coordinates, fill=False, edgecolor="black"))

axes.autoscale_view()
axes.set_aspect("equal")
plt.show()
```

## Node and element labels

The triangle helper connectivity refers to positions in `X` and `Y`, not to
original Gmsh node tags. Label the plotted positions accordingly:

```python
for index, (x, y) in enumerate(zip(X, Y, strict=True)):
    axes.text(x, y, str(index))
```

To preserve original node tags, use `get_elements_2d()` and its `nodes`
dictionary instead.

## Filtering before plotting

The modern API can select elements before custom plotting:

```python
from gmshparser.api import ElementType

surface_triangles = mesh.elements.where(
    element_type=ElementType.TRIANGLE,
    dimension=2,
)
for triangle in surface_triangles:
    coordinates = [node.coordinates[:2] for node in triangle]
```

The convenience helpers currently operate on the complete mesh. Direct
collection filtering is useful when plotting only selected entities.

## Large meshes

All helpers construct Python lists and load their result in memory. For dense
meshes, plotting every edge may be slow and visually unhelpful. Consider
plotting only selected entities or a subset of elements.

## API reference

See [Helpers API](../api/helpers.md) for the exact return values of each helper.
