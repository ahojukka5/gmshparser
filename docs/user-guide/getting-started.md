# Getting Started

gmshparser is a lightweight Python library for reading ASCII Gmsh `.msh`
files. It parses the mesh into objects representing nodes, elements, and their
entities.

## Requirements

- Python 3.12 or newer
- no runtime dependencies for parsing
- matplotlib only for the optional visualization examples

## Supported files

The parser detects these MSH versions automatically:

- 1.0
- 2.0, 2.1, and 2.2
- 4.0 and 4.1

Only ASCII MSH files are supported. See [Supported Formats](supported-formats.md)
for details and limitations.

## Install

```bash
uv add gmshparser
```

or:

```bash
pip install gmshparser
```

## Parse a mesh

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")
print(f"MSH version: {mesh.get_version()}")
print(f"Nodes: {mesh.get_number_of_nodes()}")
print(f"Elements: {mesh.get_number_of_elements()}")
```

## Inspect nodes

```python
for entity in mesh.get_node_entities():
    for node in entity.get_nodes():
        print(node.get_tag(), node.get_coordinates())
```

## Inspect elements

```python
for entity in mesh.get_element_entities():
    element_type = entity.get_element_type()
    for element in entity.get_elements():
        print(element.get_tag(), element_type, element.get_connectivity())
```

## Next steps

1. [Installation and development setup](installation.md)
2. [Basic API usage](basic-usage.md)
3. [Command-line interface](cli.md)
4. [Visualization helpers](visualization.md)
5. [Repository test meshes](https://github.com/ahojukka5/gmshparser/tree/master/testdata)

For bugs or unsupported files, open an issue and attach the smallest mesh that
reproduces the problem.
