# Visualization

gmshparser includes helper functions for visualizing 2D meshes using matplotlib.

!!! note
    Visualization requires matplotlib. Install it with:
    ```bash
    pip install matplotlib
    ```

## Quick Start

```python
import gmshparser
import matplotlib.pyplot as plt

# Parse mesh
mesh = gmshparser.parse("mesh.msh")

# Extract triangle data
X, Y, T = gmshparser.helpers.get_triangles(mesh)

# Plot
plt.triplot(X, Y, T, 'k-', linewidth=0.5)
plt.axis('equal')
plt.show()
```

## Visualizing Triangular Meshes

The `get_triangles()` helper extracts triangular elements:

```python
import gmshparser
import matplotlib.pyplot as plt
from gmshparser.helpers import get_triangles

mesh = gmshparser.parse("data/example_mesh.msh")
X, Y, T = get_triangles(mesh)

plt.figure(figsize=(10, 8))
plt.triplot(X, Y, T, color='black', linewidth=0.5)
plt.title(f"Triangular Mesh ({len(T)} triangles)")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("triangle_mesh.png", dpi=300)
plt.show()
```

## Visualizing Quadrilateral Meshes

For meshes with quadrilateral elements:

```python
import gmshparser
import matplotlib.pyplot as plt
from gmshparser.helpers import get_quads

mesh = gmshparser.parse("quad_mesh.msh")
X, Y, Q = get_quads(mesh)

fig, ax = plt.subplots(figsize=(10, 8))

# Plot each quad
for quad in Q:
    nodes = quad
    x_coords = [X[n-1] for n in nodes] + [X[nodes[0]-1]]  # Close the quad
    y_coords = [Y[n-1] for n in nodes] + [Y[nodes[0]-1]]
    ax.plot(x_coords, y_coords, 'k-', linewidth=0.5)

# Plot nodes
ax.plot(X, Y, 'ro', markersize=3, label='Nodes')

ax.set_title(f"Quadrilateral Mesh ({len(Q)} quads)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.axis('equal')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig("quad_mesh.png", dpi=300)
plt.show()
```

## Visualizing Mixed Meshes

For meshes containing both triangles and quads:

```python
import gmshparser
import matplotlib.pyplot as plt
from gmshparser.helpers import get_elements_2d

mesh = gmshparser.parse("mixed_mesh.msh")
X, Y, triangles, quads = get_elements_2d(mesh)

fig, ax = plt.subplots(figsize=(12, 10))

# Plot triangles
if triangles:
    ax.triplot(X, Y, triangles, 'b-', linewidth=0.5, label='Triangles')

# Plot quads
for quad in quads:
    x_coords = [X[n-1] for n in quad] + [X[quad[0]-1]]
    y_coords = [Y[n-1] for n in quad] + [Y[quad[0]-1]]
    ax.plot(x_coords, y_coords, 'r-', linewidth=0.5)

# Add custom legend for quads
from matplotlib.lines import Line2D
handles = [Line2D([0], [0], color='b', linewidth=0.5, label='Triangles'),
           Line2D([0], [0], color='r', linewidth=0.5, label='Quads')]
ax.legend(handles=handles)

ax.set_title(f"Mixed Mesh ({len(triangles)} triangles, {len(quads)} quads)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.axis('equal')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("mixed_mesh.png", dpi=300)
plt.show()
```

## Advanced Plotting Options

### Add Node Labels

```python
import gmshparser
import matplotlib.pyplot as plt
from gmshparser.helpers import get_triangles

mesh = gmshparser.parse("mesh.msh")
X, Y, T = get_triangles(mesh)

fig, ax = plt.subplots(figsize=(12, 10))
ax.triplot(X, Y, T, 'k-', linewidth=0.5)

# Label nodes
for i, (x, y) in enumerate(zip(X, Y), start=1):
    ax.text(x, y, str(i), fontsize=8, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

ax.set_title("Mesh with Node Labels")
ax.axis('equal')
plt.tight_layout()
plt.show()
```

### Add Element Labels

```python
import gmshparser
import matplotlib.pyplot as plt
import numpy as np
from gmshparser.helpers import get_triangles

mesh = gmshparser.parse("mesh.msh")
X, Y, T = get_triangles(mesh)

fig, ax = plt.subplots(figsize=(12, 10))
ax.triplot(X, Y, T, 'k-', linewidth=0.5)

# Label elements at their centroids
for i, tri in enumerate(T, start=1):
    x_center = np.mean([X[n] for n in tri])
    y_center = np.mean([Y[n] for n in tri])
    ax.text(x_center, y_center, str(i), fontsize=8, ha='center', va='center',
            color='red')

ax.set_title("Mesh with Element Labels")
ax.axis('equal')
plt.tight_layout()
plt.show()
```

### Color by Element Property

```python
import gmshparser
import matplotlib.pyplot as plt
import numpy as np
from gmshparser.helpers import get_triangles

mesh = gmshparser.parse("mesh.msh")
X, Y, T = get_triangles(mesh)

# Create some artificial property (e.g., element area)
areas = []
for tri in T:
    x_coords = [X[n] for n in tri]
    y_coords = [Y[n] for n in tri]
    # Simple area calculation
    area = 0.5 * abs((x_coords[1]-x_coords[0])*(y_coords[2]-y_coords[0]) - 
                     (x_coords[2]-x_coords[0])*(y_coords[1]-y_coords[0]))
    areas.append(area)

fig, ax = plt.subplots(figsize=(12, 10))
tpc = ax.tripcolor(X, Y, T, facecolors=areas, edgecolors='k', linewidth=0.5)
fig.colorbar(tpc, ax=ax, label='Element Area')
ax.set_title("Mesh Colored by Element Area")
ax.axis('equal')
plt.tight_layout()
plt.show()
```

## Exporting Figures

### High-Resolution PNG

```python
plt.savefig("mesh.png", dpi=300, bbox_inches='tight')
```

### Vector Graphics (PDF/SVG)

```python
plt.savefig("mesh.pdf", bbox_inches='tight')  # PDF
plt.savefig("mesh.svg", bbox_inches='tight')  # SVG
```

### Multiple Formats

```python
for fmt in ['png', 'pdf', 'svg']:
    plt.savefig(f"mesh.{fmt}", dpi=300, bbox_inches='tight')
```

## Complete Example Script

Here's a complete example that creates a publication-quality figure:

```python
import gmshparser
import matplotlib.pyplot as plt
from gmshparser.helpers import get_triangles

# Parse mesh
mesh = gmshparser.parse("data/example_mesh.msh")
X, Y, T = get_triangles(mesh)

# Create figure with publication settings
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'serif'
plt.rcParams['lines.linewidth'] = 0.5

fig, ax = plt.subplots(figsize=(8, 6))

# Plot mesh
ax.triplot(X, Y, T, color='black', linewidth=0.5)

# Styling
ax.set_xlabel('X coordinate [m]', fontsize=14)
ax.set_ylabel('Y coordinate [m]', fontsize=14)
ax.set_title(f'Finite Element Mesh\n{len(T)} triangular elements', fontsize=16)
ax.axis('equal')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add statistics
stats_text = f"Nodes: {len(X)}\nElements: {len(T)}"
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('publication_mesh.png', dpi=300, bbox_inches='tight')
plt.savefig('publication_mesh.pdf', bbox_inches='tight')
plt.show()

print("Figures saved: publication_mesh.png, publication_mesh.pdf")
```

## Interactive Visualization

For interactive exploration:

```python
import gmshparser
import matplotlib.pyplot as plt
from gmshparser.helpers import get_triangles

mesh = gmshparser.parse("mesh.msh")
X, Y, T = get_triangles(mesh)

plt.figure(figsize=(12, 10))
plt.triplot(X, Y, T, 'k-', linewidth=0.5)
plt.axis('equal')
plt.title("Interactive Mesh (use zoom/pan tools)")

# Enable interactive mode
plt.ion()
plt.show()

# Keep window open
input("Press Enter to close...")
```

## Troubleshooting

### matplotlib Not Found

```bash
pip install matplotlib
```

### Empty Plot

Check that your mesh contains 2D elements:

```python
mesh = gmshparser.parse("mesh.msh")
print(f"Element entities: {mesh.get_number_of_element_entities()}")
for entity in mesh.get_element_entities():
    print(f"Element type: {entity.get_element_type()}")
```

### Memory Issues with Large Meshes

For very large meshes, plot only a subset:

```python
X, Y, T = get_triangles(mesh)
# Plot only first 1000 elements
T_subset = T[:1000]
plt.triplot(X, Y, T_subset, 'k-')
```

## Next Steps

- Check the [API Reference](../api/helpers.md) for helper functions
- Learn about [Supported Formats](supported-formats.md)
- View [example scripts](https://github.com/ahojukka5/gmshparser/tree/master/examples)
