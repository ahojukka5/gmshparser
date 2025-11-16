# API Reference

gmshparser provides a simple, clean API for parsing Gmsh mesh files.

## Main Functions

### parse()

Parse a Gmsh mesh file and return a Mesh object.

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")
```

**Parameters:**

- `filename` (str): Path to the `.msh` file

**Returns:**

- `Mesh`: Parsed mesh object

**Raises:**

- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If file format is unsupported or invalid

## Core Classes

### Mesh

The main mesh container class.

For detailed API, see [Mesh API](mesh.md).

### Node & NodeEntity

Classes for node data organization.

### Element & ElementEntity

Classes for element data organization.

### Parsers

Parser classes for different mesh sections.

See [Parsers API](parsers.md) for details.

## Helper Functions

Utility functions for common mesh operations.

See [Helpers API](helpers.md) for details.

## Quick Reference

```python
import gmshparser

# Parse mesh
mesh = gmshparser.parse("mesh.msh")

# Get mesh info
mesh.get_version()
mesh.get_number_of_nodes()
mesh.get_number_of_elements()

# Access nodes
for entity in mesh.get_node_entities():
    for node in entity.get_nodes():
        node.get_tag()
        node.get_coordinates()

# Access elements
for entity in mesh.get_element_entities():
    for element in entity.get_elements():
        element.get_tag()
        element.get_connectivity()

# Helper functions
from gmshparser.helpers import get_triangles, get_quads, get_elements_2d

X, Y, T = get_triangles(mesh)
X, Y, Q = get_quads(mesh)
X, Y, triangles, quads = get_elements_2d(mesh)
```

## Next Steps

- [Mesh API](mesh.md) - Complete Mesh class reference
- [Parsers API](parsers.md) - Parser classes
- [Helpers API](helpers.md) - Utility functions
