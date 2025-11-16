# gmshparser

[![Python CI - Status][gh-ci-img]][gh-ci-url]
[![PyPI - Version][pypi-img]][pypi-url]
[![PyPI - Downloads][pypi-dl-img]][pypi-dl-url]
[![Coverage Status][coveralls-img]][coveralls-url]
[![Documentation Status][documentation-img]][documentation-url]

**A lightweight Python package for parsing Gmsh .msh mesh files**

Package author: Jukka Aho ([@ahojukka5](https://github.com/ahojukka5))

## Overview

gmshparser is a small Python package designed to do one thing well: parse [Gmsh](https://gmsh.info/)
mesh file formats. With **no external dependencies** and a clean API, it provides a simple
stand-alone solution for importing meshes into your FEM research code.

## Key Features

- ✅ **Multiple format support**: MSH 1.0, 2.0, 2.1, 2.2, 4.0, and 4.1
- ✅ **Automatic version detection**: No need to specify format version
- ✅ **Zero dependencies**: Pure Python implementation
- ✅ **100% test coverage**: Thoroughly tested and documented
- ✅ **Command-line interface**: Extract mesh data from terminal
- ✅ **Easy visualization**: Built-in matplotlib helpers

## Quick Start

Install the package:

```bash
pip install gmshparser
```

Parse a mesh file:

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")
print(f"Loaded mesh with {mesh.get_number_of_nodes()} nodes "
      f"and {mesh.get_number_of_elements()} elements")
```

## Supported Formats

gmshparser supports all major versions of the Gmsh MSH file format:

| Version | Description | Status |
|---------|-------------|--------|
| **MSH 1.0** | Legacy format with `$NOD`/`$ELM` sections | ✅ Supported |
| **MSH 2.0** | Standard format with `$MeshFormat` | ✅ Supported |
| **MSH 2.1** | Added `$PhysicalNames` support | ✅ Supported |
| **MSH 2.2** | Compatible with 2.0/2.1 | ✅ Supported |
| **MSH 4.0** | Modern format with `$Entities` | ✅ Supported |
| **MSH 4.1** | Latest version | ✅ Supported |

## Documentation Sections

### [User Guide](user-guide/getting-started.md)

Learn how to install, use, and visualize meshes with gmshparser.

### [Developer Guide](developer-guide/contributing.md)

Contribute to the project, understand the architecture, and write custom parsers.

### [API Reference](api/overview.md)

Complete API documentation for all classes and functions.

## Project Links

- **Source Code**: [GitHub Repository](https://github.com/ahojukka5/gmshparser)
- **Issue Tracker**: [GitHub Issues](https://github.com/ahojukka5/gmshparser/issues)
- **PyPI Package**: [gmshparser on PyPI](https://pypi.org/project/gmshparser)
- **License**: [MIT License](about/license.md)

## Quick Example

```python
import gmshparser

# Parse mesh file
mesh = gmshparser.parse("data/testmesh.msh")

# Access nodes
for entity in mesh.get_node_entities():
    for node in entity.get_nodes():
        print(f"Node {node.get_tag()}: {node.get_coordinates()}")

# Access elements
for entity in mesh.get_element_entities():
    for element in entity.get_elements():
        print(f"Element {element.get_tag()}: {element.get_connectivity()}")
```

## Contributing

Contributions are always welcome! Please see our [Contributing Guide](developer-guide/contributing.md)
for details on how to get started.

[gh-ci-img]: https://github.com/ahojukka5/gmshparser/workflows/Python%20CI/badge.svg
[gh-ci-url]: https://github.com/ahojukka5/gmshparser/actions
[coveralls-img]: https://coveralls.io/repos/github/ahojukka5/gmshparser/badge.svg?branch=master
[coveralls-url]: https://coveralls.io/github/ahojukka5/gmshparser?branch=master
[pypi-img]: https://img.shields.io/pypi/v/gmshparser
[pypi-url]: https://pypi.org/project/gmshparser
[pypi-dl-img]: https://img.shields.io/pypi/dm/gmshparser
[pypi-dl-url]: https://pypi.org/project/gmshparser
[documentation-img]: https://readthedocs.org/projects/gmshparser/badge/?version=latest
[documentation-url]: https://gmshparser.readthedocs.io/en/latest/?badge=latest
