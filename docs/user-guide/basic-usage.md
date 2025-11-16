# Basic Usage

This guide covers the fundamental usage patterns of gmshparser.

## Parsing a Mesh File

The primary function you'll use is `gmshparser.parse()`:

```python
import gmshparser

mesh = gmshparser.parse("path/to/mesh.msh")
```

This automatically detects the file format version and returns a `Mesh` object.

## Mesh Information

After parsing, you can query basic mesh information:

```python
# Get mesh metadata
print(f"Mesh name: {mesh.get_name()}")
print(f"Mesh version: {mesh.get_version()}")
print(f"Number of nodes: {mesh.get_number_of_nodes()}")
print(f"Number of elements: {mesh.get_number_of_elements()}")

# Get node tag ranges
print(f"Min node tag: {mesh.get_min_node_tag()}")
print(f"Max node tag: {mesh.get_max_node_tag()}")

# Get element tag ranges
print(f"Min element tag: {mesh.get_min_element_tag()}")
print(f"Max element tag: {mesh.get_max_element_tag()}")

# Get entity counts
print(f"Node entities: {mesh.get_number_of_node_entities()}")
print(f"Element entities: {mesh.get_number_of_element_entities()}")
```

## Working with Nodes

Nodes in gmshparser are organized by entities. Here's how to access them:

### Iterate All Nodes

```python
for entity in mesh.get_node_entities():
    for node in entity.get_nodes():
        node_id = node.get_tag()
        coords = node.get_coordinates()
        x, y, z = coords
        print(f"Node {node_id}: ({x}, {y}, {z})")
```

### Get Specific Node Data

```python
# Get all nodes from first entity
first_entity = mesh.get_node_entities()[0]
nodes = first_entity.get_nodes()

# Access node properties
for node in nodes:
    tag = node.get_tag()          # Node ID
    coords = node.get_coordinates()  # (x, y, z) tuple
    x = coords[0]
    y = coords[1]
    z = coords[2]
```

### Entity Information

```python
for entity in mesh.get_node_entities():
    dimension = entity.get_dimension()
    entity_tag = entity.get_tag()
    num_nodes = entity.get_number_of_nodes()
    print(f"Entity {entity_tag} (dim={dimension}): {num_nodes} nodes")
```

## Working with Elements

Elements are also organized by entities:

### Iterate All Elements

```python
for entity in mesh.get_element_entities():
    element_type = entity.get_element_type()
    print(f"Element type: {element_type}")
    
    for element in entity.get_elements():
        elem_id = element.get_tag()
        connectivity = element.get_connectivity()
        print(f"Element {elem_id}: nodes {connectivity}")
```

### Element Types

Gmsh uses numeric codes for element types:

| Code | Element Type | Nodes |
|------|-------------|--------|
| 15 | Point | 1 |
| 1 | Line | 2 |
| 2 | Triangle | 3 |
| 3 | Quadrangle | 4 |
| 4 | Tetrahedron | 4 |
| 5 | Hexahedron | 8 |
| 8 | Line (3-node) | 3 |
| 9 | Triangle (6-node) | 6 |
| ... | ... | ... |

See the [Gmsh documentation](https://gmsh.info/doc/texinfo/gmsh.html#MSH-file-format) for a complete list.

### Filter Elements by Type

```python
# Get all triangular elements
for entity in mesh.get_element_entities():
    if entity.get_element_type() == 2:  # Triangle
        for element in entity.get_elements():
            print(f"Triangle {element.get_tag()}: {element.get_connectivity()}")
```

## Using Helper Functions

gmshparser provides helper functions for common tasks:

### Extract Triangles for Plotting

```python
from gmshparser.helpers import get_triangles

mesh = gmshparser.parse("mesh.msh")
X, Y, T = get_triangles(mesh)

# X, Y: coordinate arrays
# T: connectivity array for matplotlib.triplot
```

### Extract Quadrilaterals

```python
from gmshparser.helpers import get_quads

mesh = gmshparser.parse("mesh.msh")
X, Y, Q = get_quads(mesh)

# Q: quadrilateral connectivity array
```

### Extract All 2D Elements

```python
from gmshparser.helpers import get_elements_2d

mesh = gmshparser.parse("mesh.msh")
X, Y, triangles, quads = get_elements_2d(mesh)

# Returns both triangles and quads
```

## Practical Examples

### Example 1: Export Nodes to CSV

```python
import gmshparser
import csv

mesh = gmshparser.parse("mesh.msh")

with open("nodes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "X", "Y", "Z"])
    
    for entity in mesh.get_node_entities():
        for node in entity.get_nodes():
            tag = node.get_tag()
            x, y, z = node.get_coordinates()
            writer.writerow([tag, x, y, z])
```

### Example 2: Count Element Types

```python
import gmshparser
from collections import Counter

mesh = gmshparser.parse("mesh.msh")

element_types = Counter()
for entity in mesh.get_element_entities():
    elem_type = entity.get_element_type()
    elem_count = entity.get_number_of_elements()
    element_types[elem_type] += elem_count

for elem_type, count in element_types.items():
    print(f"Type {elem_type}: {count} elements")
```

### Example 3: Build a Connectivity Matrix

```python
import gmshparser
import numpy as np

mesh = gmshparser.parse("mesh.msh")

# Collect all triangular elements
triangles = []
for entity in mesh.get_element_entities():
    if entity.get_element_type() == 2:  # Triangle
        for element in entity.get_elements():
            triangles.append(element.get_connectivity())

# Convert to numpy array
connectivity = np.array(triangles)
print(f"Triangle connectivity shape: {connectivity.shape}")
```

## Working with Different MSH Versions

gmshparser handles version differences automatically:

```python
# Works with any supported version (1.0, 2.0, 2.1, 2.2, 4.0, 4.1)
mesh = gmshparser.parse("any_version.msh")

# Check which version was detected
version = mesh.get_version()
print(f"Detected MSH version: {version}")
```

The API remains consistent regardless of the file format version.

## Error Handling

Handle parsing errors gracefully:

```python
import gmshparser

try:
    mesh = gmshparser.parse("mesh.msh")
except FileNotFoundError:
    print("Mesh file not found")
except Exception as e:
    print(f"Error parsing mesh: {e}")
```

## Next Steps

- Learn about the [Command Line Interface](cli.md)
- Explore [Visualization options](visualization.md)
- Check the [API Reference](../api/overview.md)
