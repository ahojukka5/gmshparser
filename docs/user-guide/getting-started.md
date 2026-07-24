# Getting Started

gmshparser is a lightweight Python library for reading ASCII Gmsh `.msh`
files. New code uses an immutable, Pythonic model; the original mutable model is
retained for compatibility.

## Requirements

- Python 3.12 or newer
- no runtime dependencies for parsing
- matplotlib only for optional visualization examples

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

## Read a mesh

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")
print(f"MSH version: {mesh.version}")
print(f"Nodes: {len(mesh.nodes)}")
print(f"Elements: {len(mesh.elements)}")
```

## Inspect nodes

```python
for node in mesh.nodes:
    print(node.tag, node.coordinates)
```

Look up a node by its Gmsh tag:

```python
node = mesh.nodes[42]
print(node.x, node.y, node.z)
```

## Inspect and filter elements

```python
for element in mesh.elements:
    print(element.tag, element.element_type, element.node_tags)

triangles = mesh.elements.by_type(2)
surface_elements = mesh.elements.where(dimension=2)
```

## Existing applications

The original API remains available:

```python
legacy_mesh = gmshparser.parse("mesh.msh")
print(legacy_mesh.get_number_of_nodes())
```

## Next steps

1. [Pythonic API](pythonic-api.md)
2. [Basic API usage](basic-usage.md)
3. [Installation and development setup](installation.md)
4. [Command-line interface](cli.md)
5. [Visualization helpers](visualization.md)
6. [Repository test meshes](https://github.com/ahojukka5/gmshparser/tree/master/testdata)

For bugs or unsupported files, open an issue and attach the smallest mesh that
reproduces the problem.
