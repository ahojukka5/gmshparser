# Getting Started

Welcome to gmshparser! This guide will help you get started with parsing Gmsh mesh files in Python.

## What is gmshparser?

gmshparser is a lightweight Python library for reading Gmsh `.msh` files. It focuses on doing one thing well: parsing mesh files with a clean, simple API.

## Why gmshparser?

- **No external dependencies**: Pure Python implementation
- **Universal format support**: Works with MSH 1.0 through 4.1
- **Automatic detection**: Detects file format version automatically
- **Well tested**: 100% test coverage with 34+ test cases
- **Easy to use**: Simple, intuitive API

## What can you do with gmshparser?

- Parse Gmsh mesh files of any supported version
- Extract nodes and their coordinates
- Extract elements and their connectivity
- Access physical groups and entities
- Export mesh data for other FEM codes
- Visualize 2D meshes using matplotlib

## System Requirements

- Python 3.8.1 or later
- No external dependencies required for core functionality
- matplotlib (optional, for visualization)

## Next Steps

1. [Install gmshparser](installation.md)
2. [Learn basic usage](basic-usage.md)
3. [Try the command-line interface](cli.md)
4. [Visualize your meshes](visualization.md)

## Quick Example

Here's a simple example to get you started:

```python
import gmshparser

# Parse a mesh file
mesh = gmshparser.parse("my_mesh.msh")

# Print mesh information
print(f"Mesh version: {mesh.get_version()}")
print(f"Number of nodes: {mesh.get_number_of_nodes()}")
print(f"Number of elements: {mesh.get_number_of_elements()}")

# Access first node
for entity in mesh.get_node_entities():
    for node in entity.get_nodes():
        print(f"First node: {node.get_tag()} at {node.get_coordinates()}")
        break
    break
```

## Getting Help

If you encounter issues or have questions:

- Check the [API Reference](../api/overview.md)
- Review [examples in the repository](https://github.com/ahojukka5/gmshparser/tree/master/examples)
- [Open an issue on GitHub](https://github.com/ahojukka5/gmshparser/issues)
- Contact the author: <ahojukka5@gmail.com>
