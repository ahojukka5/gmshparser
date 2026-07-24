# Compatibility Mesh API

This page documents the original mutable parser-oriented model returned by
`gmshparser.parse()`. New code should normally use `gmshparser.read()` and the
[modern API](modern.md).

::: gmshparser.mesh.Mesh
    options:
      show_source: true
      heading_level: 2

## Usage examples

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")

version = mesh.get_version()
is_ascii = mesh.get_ascii()
num_nodes = mesh.get_number_of_nodes()
num_elements = mesh.get_number_of_elements()
node_entities = mesh.get_node_entities()
element_entities = mesh.get_element_entities()
```

The compatibility API is retained for existing applications and for low-level
parser development. It remains mutable and mirrors the internal MSH entity-block
structure.

Equivalent modern access is considerably flatter:

```python
mesh = gmshparser.read("mesh.msh")

version = mesh.version
is_ascii = mesh.is_ascii
num_nodes = len(mesh.nodes)
num_elements = len(mesh.elements)
```
