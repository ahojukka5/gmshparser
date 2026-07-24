# Error handling

Both `gmshparser.read()` and the compatibility `gmshparser.parse()` entry point
raise the same structured parser errors.

```python
import gmshparser

try:
    mesh = gmshparser.read("mesh.msh")
except gmshparser.ParseError as error:
    print(error)
```

A formatted error includes the source name, line number, and current MSH section
when those values are available:

```text
broken.msh:127 [$Elements]: element 42 requires 3 nodes, got 4
```

The same information is available as attributes:

```python
print(error.filename)
print(error.line_number)
print(error.section)
print(error.line)
print(error.message)
```

For streams without a filesystem path, pass a useful name explicitly:

```python
from io import StringIO

mesh = gmshparser.read(StringIO(msh_text), name="generated.msh")
```

## Error hierarchy

All public gmshparser exceptions derive from `GmshError`. Input and parser
failures derive from `ParseError`:

```text
GmshError
└── ParseError
    ├── UnsupportedVersionError
    ├── UnsupportedBinaryFormatError
    ├── UnexpectedEndOfFileError
    ├── InvalidSectionError
    ├── InvalidNodeError
    ├── InvalidElementError
    │   ├── InvalidElementConnectivityError
    │   └── UnknownElementTypeError
    └── InvalidMeshError
```

Catch a specific type when the application can recover from it:

```python
try:
    mesh = gmshparser.read("mesh.msh")
except gmshparser.UnsupportedBinaryFormatError:
    print("Export the mesh as ASCII in Gmsh and retry")
except gmshparser.UnsupportedVersionError as error:
    print(error)
except gmshparser.InvalidElementConnectivityError as error:
    print(error.line)
```

## Backward compatibility

`ParseError` also inherits from `ValueError`. Existing applications that used a
broad handler continue to work:

```python
try:
    mesh = gmshparser.read("mesh.msh")
except ValueError:
    ...
```

New code should normally catch `ParseError` or a more specific subclass so that
unrelated `ValueError` exceptions are not hidden.

## Validation performed

The parser validates, among other things:

- supported MSH versions and ASCII file type
- section headers and numeric fields
- declared node, element, entity, and physical-name counts
- node and element record widths
- known element dimensions and connectivity sizes
- section end markers such as `$EndNodes` and `$EndElements`
- unexpected end of file inside a declared section

The parser does not print failures to stdout or stderr. Applications decide how
to log or display the exception.
