# Helpers API

Utility functions for common mesh operations.

## get_triangles()

Extract triangular elements from mesh for plotting.

::: gmshparser.helpers.get_triangles
    options:
      show_source: true
      heading_level: 3

**Example:**

```python
import gmshparser
import matplotlib.pyplot as plt
from gmshparser.helpers import get_triangles

mesh = gmshparser.parse("mesh.msh")
X, Y, T = get_triangles(mesh)

plt.triplot(X, Y, T)
plt.show()
```

## get_quads()

Extract quadrilateral elements from mesh.

::: gmshparser.helpers.get_quads
    options:
      show_source: true
      heading_level: 3

**Example:**

```python
from gmshparser.helpers import get_quads

mesh = gmshparser.parse("quad_mesh.msh")
X, Y, Q = get_quads(mesh)

# Plot quads
for quad in Q:
    x = [X[n-1] for n in quad] + [X[quad[0]-1]]
    y = [Y[n-1] for n in quad] + [Y[quad[0]-1]]
    plt.plot(x, y, 'k-')
```

## get_elements_2d()

Extract all 2D elements (triangles and quads).

::: gmshparser.helpers.get_elements_2d
    options:
      show_source: true
      heading_level: 3

**Example:**

```python
from gmshparser.helpers import get_elements_2d

mesh = gmshparser.parse("mixed_mesh.msh")
X, Y, triangles, quads = get_elements_2d(mesh)

print(f"Found {len(triangles)} triangles and {len(quads)} quads")
```

## Utility Functions

### parse_ints()

Parse space-separated integers from string.

### parse_floats()

Parse space-separated floats from string.

## See Also

- [Visualization Guide](../user-guide/visualization.md)
- [Basic Usage](../user-guide/basic-usage.md)
