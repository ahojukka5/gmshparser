# Welcome to gmshparser's documentation!


gmshparser is a small Python package which aims to do only one thing: parses
Gmsh .msh file format. Package does not have any dependencies to other packages
and it tries to be a simple stand-alone solution to a common problem: how to
import mesh to your favorite research FEM code?

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