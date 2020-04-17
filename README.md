# gmshparser - parse Gmsh .msh file format

[![Build Status][travis-img]][travis-url]
[![Coverate Status][coveralls-img]][coveralls-url]

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

[travis-img]: https://travis-ci.com/ahojukka5/gmshparser.svg?branch=master
[travis-url]: https://travis-ci.com/ahojukka5/gmshparser
[coveralls-img]: https://coveralls.io/repos/github/ahojukka5/gmshparser/badge.svg?branch=master
[coveralls-url]: https://coveralls.io/github/ahojukka5/gmshparser?branch=master
