# Welcome to gmshparser's documentation!

Package author: Jukka Aho (@ahojukka5)

Gmshparser is a small Python package which aims to do only one thing: parse Gmsh
mesh file format. Package does not have any external dependencies to other
packages and it aims to be a simple stand-alone solution for a common problem:
how to import mesh to your favourite research FEM code?

Project is hosted on GitHub: <https://github.com/ahojukka5/gmshparser>

## Installing package

Using pip:

```bash
pip install gmshparser
```

## Usage

```python
import gmshparser
gmshparser.parse("testdata.msh")
```

## Contributing to project

Like in other open source projects, contributions are always welcome to this
too! If you have some great ideas how to make this package better, feature
requests etc., you can open an issue on gmshparser's [issue tracker][issues] or
contact me (ahojukka5 at gmail.com) directly.

[issues]: https://github.com/ahojukka5/gmshparser/issues
[gmsh]: https://gmsh.info/
