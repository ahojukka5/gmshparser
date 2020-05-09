# gmshparser - parse Gmsh .msh file format

![Python CI](https://github.com/ahojukka5/gmshparser/workflows/Python%20CI/badge.svg)
[![Build Status][travis-img]][travis-url]
[![Coverate Status][coveralls-img]][coveralls-url]
[![Documentation Status][documentation-img]][documentation-url]

Package author: Jukka Aho (@ahojukka5)

Gmshparser is a small Python package which aims to do only one thing: parse Gmsh
mesh file format. Package does not have any external dependencies to other
packages and it aims to be a simple stand-alone solution for a common problem:
how to import mesh to your favourite research FEM code?

Project documentation is located at: [https://gmshparser.readthedocs.io/](https://gmshparser.readthedocs.io/)

## Installing package

Using pip:

```bash
pip install gmshparser
```

## Usage

To read mesh into `Mesh` object, use command `parse`:

```python
import gmshparser
mesh = gmshparser.parse("data/testmesh.msh")
print(mesh)
```

Output is

```text
Mesh name: data/testmesh.msh
Mesh version: 4.1
Number of nodes: 6
Minimum node tag: 1
Maximum node tag: 6
Number of node entities: 1
Number of elements: 2
Minimum element tag: 1
Maximum element tag: 2
Number of element entities: 1
```

For further information on how to access nodes, elements, physical groups etc.
look the [documentation](https://gmshparser.readthedocs.io/).

## Contributing to project

Like in other open source projects, contributions are always welcome to this
too! If you have some great ideas how to make this package better, feature
requests etc., you can open an issue on gmshparser's [issue tracker][issues] or
contact me (ahojukka5 at gmail.com) directly.

[travis-img]: https://travis-ci.com/ahojukka5/gmshparser.svg?branch=master
[travis-url]: https://travis-ci.com/ahojukka5/gmshparser
[coveralls-img]: https://coveralls.io/repos/github/ahojukka5/gmshparser/badge.svg?branch=master
[coveralls-url]: https://coveralls.io/github/ahojukka5/gmshparser?branch=master
[documentation-img]: https://readthedocs.org/projects/gmshparser/badge/?version=latest
[documentation-url]: https://gmshparser.readthedocs.io/en/latest/?badge=latest
[issues]: https://github.com/ahojukka5/gmshparser/issues
[gmsh]: https://gmsh.info/
