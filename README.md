# gmshparser - parse Gmsh .msh file format

[![Build Status][travis-img]][travis-url]
[![Coverate Status][coveralls-img]][coveralls-url]
[![Documentation Status][documentation-img]][documentation-url]

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
