# Basic Usage

## Parse a mesh

```python
import gmshparser

mesh = gmshparser.parse("path/to/mesh.msh")
```

The parser detects the supported MSH version automatically and returns a
`Mesh` object.

## Mesh metadata

```python
print(mesh.get_name())
print(mesh.get_version())
print(mesh.get_number_of_nodes())
print(mesh.get_number_of_elements())
print(mesh.get_min_node_tag(), mesh.get_max_node_tag())
print(mesh.get_min_element_tag(), mesh.get_max_element_tag())
print(mesh.get_number_of_node_entities())
print(mesh.get_number_of_element_entities())
```

## Nodes

Nodes are grouped into node entities:

```python
for entity in mesh.get_node_entities():
    print(
        "entity",
        entity.get_dimension(),
        entity.get_tag(),
        entity.get_number_of_nodes(),
    )

    for node in entity.get_nodes():
        node_id = node.get_tag()
        x, y, z = node.get_coordinates()
        print(node_id, x, y, z)
```

## Elements

Elements are grouped into element entities. The entity stores the Gmsh element
type shared by its elements:

```python
for entity in mesh.get_element_entities():
    element_type = entity.get_element_type()
    print(
        "entity",
        entity.get_dimension(),
        entity.get_tag(),
        element_type,
        entity.get_number_of_elements(),
    )

    for element in entity.get_elements():
        print(element.get_tag(), element.get_connectivity())
```

Gmsh element types are numeric. Common values include 1 for a two-node line, 2
for a three-node triangle, 3 for a four-node quadrangle, and 4 for a
four-node tetrahedron. Consult the official Gmsh MSH specification for the full
list.

## Filter by element type

```python
triangles = []
for entity in mesh.get_element_entities():
    if entity.get_element_type() == 2:
        triangles.extend(
            element.get_connectivity() for element in entity.get_elements()
        )
```

## Visualization helpers

### Triangles

`get_triangles()` returns coordinate arrays and zero-based connectivity suitable
for matplotlib:

```python
from gmshparser.helpers import get_triangles

X, Y, triangles = get_triangles(mesh)
```

### Quadrangles

`get_quads()` uses the same zero-based indexing convention:

```python
from gmshparser.helpers import get_quads

X, Y, quads = get_quads(mesh)
```

### Mixed 2D meshes

`get_elements_2d()` returns a dictionary. Its element connectivity retains the
original Gmsh node tags rather than converting them to zero-based indices:

```python
from gmshparser.helpers import get_elements_2d

data = get_elements_2d(mesh)

nodes = data["nodes"]          # node tag -> (x, y)
triangles = data["triangles"] # connectivity using node tags
quads = data["quads"]         # connectivity using node tags
node_ids = data["node_ids"]
```

See [Visualization](visualization.md) for plotting examples.

## Export nodes to CSV

```python
import csv

with open("nodes.csv", "w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["id", "x", "y", "z"])

    for entity in mesh.get_node_entities():
        for node in entity.get_nodes():
            writer.writerow([node.get_tag(), *node.get_coordinates()])
```

## Error handling

```python
try:
    mesh = gmshparser.parse("mesh.msh")
except FileNotFoundError:
    print("Mesh file not found")
except ValueError as error:
    print(f"Unsupported or invalid MSH file: {error}")
```

Unexpected or malformed section contents may also raise parsing-related Python
exceptions. When reporting such a case, include the smallest mesh file that
reproduces it.
