# Working with Meshes

This page is task-oriented. For the complete object model and filtering semantics, see [Modern Data Model](pythonic-api.md).

## Read a path

```python
import gmshparser

mesh = gmshparser.read("path/to/mesh.msh")
```

`read()` detects the supported MSH version automatically and returns an immutable `gmshparser.api.Mesh`.

## Read a text stream

```python
from io import StringIO

mesh = gmshparser.read(StringIO(msh_text), name="generated.msh")
```

The optional `name` appears in parser errors and `mesh.name`.

## Summarize a mesh

```python
print(mesh.name)
print(mesh.version)
print(mesh.dimension)
print(mesh.bounds)
print(len(mesh.nodes), len(mesh.elements), len(mesh.entities))
print(mesh.element_types)
```

`mesh.bounds` is `((xmin, ymin, zmin), (xmax, ymax, zmax))`. Empty meshes have no geometric dimension or bounds.

## Look up nodes by tag

```python
node = mesh.nodes[42]
print(node.coordinates)
print(node.entity_key)
print(node.physical_tags)
```

Integer indexing always means the original Gmsh tag. It is not a positional array index.

Use `get()` when absence is expected:

```python
node = mesh.nodes.get(42)
if node is not None:
    print(node.x, node.y, node.z)
```

## Filter nodes

```python
surface_nodes = mesh.nodes.where(dimension=2)
entity_nodes = mesh.nodes.by_entity(dimension=2, tag=7)
parametric_nodes = mesh.nodes.where(parametric=True)
physical_nodes = mesh.nodes.where(physical_tag=10)
```

Filtered collections retain normal tag lookup and parser order.

## Inspect elements

```python
from gmshparser import ElementType

for element in mesh.elements:
    print(element.tag, element.element_type, element.node_tags)
    for node in element:
        print(node.coordinates)

triangles = mesh.elements.by_type(ElementType.TRIANGLE)
```

`element.nodes` contains resolved `Node` objects. `element.node_tags` and `element.connectivity` retain the original Gmsh connectivity tags.

## Filter elements

```python
surface_quads = mesh.elements.where(
    element_type=ElementType.QUADRANGLE,
    dimension=2,
)
entity_elements = mesh.elements.by_entity(dimension=2, tag=7)
physical_elements = mesh.elements.where(physical_tag=10)
```

## Work with entities

```python
surface = mesh.entity(dimension=2, tag=7)

print(surface.nodes)
print(surface.elements)
print(surface.element_types)
print(surface.physical_tags)
```

Dimension views are available directly:

```python
print(mesh.points)
print(mesh.curves)
print(mesh.surfaces)
print(mesh.volumes)
```

Filter the complete entity collection when several conditions matter:

```python
triangle_surfaces = mesh.entities.where(
    dimension=2,
    element_type=ElementType.TRIANGLE,
    has_elements=True,
)
```

## Export nodes to CSV

```python
import csv

with open("nodes.csv", "w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["tag", "x", "y", "z"])
    writer.writerows((node.tag, *node.coordinates) for node in mesh.nodes)
```

## Build an element-to-coordinate table

```python
rows = [
    (
        element.tag,
        element.element_type,
        tuple(node.coordinates for node in element),
    )
    for element in mesh.elements
]
```

For numerical arrays and zero-based connectivity, use [NumPy Interoperability](numpy.md) instead.

## Physical and periodic metadata

Named boundaries, materials, and periodic node relations are covered in [Physical Groups and Periodicity](physical-groups.md).

## Error handling

```python
try:
    mesh = gmshparser.read("mesh.msh")
except FileNotFoundError:
    print("Mesh file not found")
except gmshparser.ParseError as error:
    print(error)
```

See [Error Handling](error-handling.md) for the complete hierarchy and source context.

## Existing compatibility applications

```python
legacy_mesh = gmshparser.parse("mesh.msh")
```

See [Migrating from the Compatibility API](migration.md) when moving existing `get_*` code to the modern model.
