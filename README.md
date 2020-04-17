# gmshparser - parse Gmsh .msh file format

[![Build Status](https://travis-ci.org/ahojukka5/gmshparser.svg?branch=master)](https://travis-ci.org/ahojukka5/gmshparser)

Package author: Jukka Aho (@ahojukka5)

This is a simple package which does only one thing: parses Gmsh .msh file
format. No external dependencies or anything extra. Just mesh parsing.

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
